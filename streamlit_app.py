"""
Store Review Sentiment — capstone entry (Streamlit).

Run from project root:
  streamlit run streamlit_app.py
"""

from __future__ import annotations

import io
import json
import sys
from datetime import datetime
from pathlib import Path

import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dotenv import load_dotenv

load_dotenv(ROOT / ".env", override=True)

from store_review.branding import ensure_branding_assets, favicon_abs_path
from store_review.config.settings import Settings
from store_review.config.theme import APP_CSS
from store_review.core.ai_providers import DEFAULT_MODELS, RichAnalyzer, resolve_api_keys
from store_review.core.analyzer import analyze_batch, dedupe_reviews
from store_review.fetchers.file_loader import load_reviews_from_dataframe
from store_review.ui.analysis_results_dashboard import render_analysis_results_dashboard
from store_review.ui.compare_panel import (
    compare_tab_has_user_input,
    execute_compare_analysis,
    merge_compare_details_for_dashboard,
    render_compare_tab,
)
from store_review.config.i18n import t
from store_review.ui.footer import render_footer
from store_review.ui.masthead import (
    SOURCE_OPTIONS,
    SOURCE_POOL_KEY,
    render_masthead,
    session_main_data_source as _session_main_data_source,
)
from store_review.ui.review_cards import render_analyzed_review_cards
from store_review.ui.store_link_panel import render_store_link_tab
from store_review.utils.exporters import df_to_csv_bytes, df_to_excel_bytes
from store_review.utils.pdf_export import (
    build_analysis_pdf_bytes,
    build_raw_pool_pdf_bytes,
    safe_pdf_filename,
)
from store_review.utils.validators import is_valid_comment


def _secrets_get(key: str):
    try:
        return st.secrets.get(key)
    except Exception:
        return None


def _prepare_pool(rows: list[dict]) -> list[dict]:
    out = []
    for r in dedupe_reviews(rows):
        t = str(r.get("text", "")).strip()
        if len(t) < 2:
            continue
        rr = dict(r)
        rr["is_valid"] = is_valid_comment(t)
        out.append(rr)
    return out


def _inject_css() -> None:
    st.markdown(f"<style>{APP_CSS}</style>", unsafe_allow_html=True)


def _max_upload_mb() -> int:
    try:
        from streamlit import config as st_config

        v = st_config.get_option("server.maxUploadSize")
        return int(v) if v is not None else 200
    except Exception:
        return 200


def _inject_file_uploader_labels_once() -> None:
    """st.file_uploader iç metinleri Streamlit API ile değiştirilemediği için üst belgede yamalama."""
    if st.session_state.get("_sr_file_uploader_label_js"):
        return
    st.session_state["_sr_file_uploader_label_js"] = True
    mb = _max_upload_mb()
    limit_txt = f"en fazla {mb} mb • csv, xlsx"
    btn_txt = "yükle"
    html = f"""
<script>
(function () {{
  const root = window.parent;
  if (!root || root.__srFileUploadLabelPatch) return;
  root.__srFileUploadLabelPatch = true;
  const doc = root.document;
  const LIMIT = {json.dumps(limit_txt)};
  const BTN = {json.dumps(btn_txt)};
  function patch() {{
    doc.querySelectorAll('[data-testid="stFileUploader"]').forEach((w) => {{
      const zone = w.querySelector('[data-testid="stFileUploaderDropzone"]');
      const b = zone && zone.querySelector("button");
      if (b) {{
        const tw = doc.createTreeWalker(b, NodeFilter.SHOW_TEXT, null);
        let n;
        while ((n = tw.nextNode())) {{
          const v = (n.nodeValue || "").trim();
          if (!v) continue;
          if (/browse|upload|choose file|select file|dizin|directory|files here/i.test(v))
            n.nodeValue = BTN;
        }}
      }}
      const ins = w.querySelector('[data-testid="stFileUploaderDropzoneInstructions"]');
      if (ins) {{
        let hit = false;
        const tw = doc.createTreeWalker(ins, NodeFilter.SHOW_TEXT, null);
        let n;
        while ((n = tw.nextNode())) {{
          if (/per\\s*file/i.test(n.nodeValue || "")) {{
            n.nodeValue = LIMIT;
            hit = true;
            break;
          }}
        }}
        if (!hit) {{
          ins.querySelectorAll("*").forEach((el) => {{
            if (el.children.length === 0 && /per\\s*file/i.test(el.textContent || ""))
              el.textContent = LIMIT;
          }});
        }}
      }}
    }});
  }}
  const obs = new MutationObserver(() => patch());
  if (doc.body) {{
    obs.observe(doc.body, {{ childList: true, subtree: true }});
    patch();
  }}
}})();
</script>
"""
    components.html(html, height=0, width=0)


def _init_split_pools() -> None:
    for k in ("store", "file", "paste"):
        if f"review_pool_{k}" not in st.session_state:
            st.session_state[f"review_pool_{k}"] = []
    if "_file_uploader_gen" not in st.session_state:
        st.session_state._file_uploader_gen = 0
    if not st.session_state.get("_pools_migrated_from_legacy"):
        legacy = st.session_state.get("review_pool")
        if isinstance(legacy, list) and legacy:
            if not st.session_state.review_pool_store:
                st.session_state.review_pool_store = list(legacy)
        st.session_state._pools_migrated_from_legacy = True


def _active_review_pool() -> list:
    label = _session_main_data_source()
    pk = SOURCE_POOL_KEY.get(label, "store")
    if pk == "compare":
        return []
    return list(st.session_state.get(f"review_pool_{pk}") or [])


def _havuz_metric_visible(src: str, pool_display_count: int) -> bool:
    """Havuzdaki yorum kutusu: yalnız ilgili sekmede veri / taslak / uygulama girişi varken."""
    if src == "Mağaza":
        typed = (st.session_state.get("sl_store_input") or "").strip()
        if typed or st.session_state.get("sl_selected_id"):
            return True
        return pool_display_count > 0
    if src == "Dosya":
        return pool_display_count > 0
    if src == "Metin":
        draft = (st.session_state.get("paste_reviews") or "").strip()
        return bool(draft or pool_display_count > 0)
    if src == "Uygulama karşılaştır":
        return compare_tab_has_user_input() or pool_display_count > 0
    return False


def main():
    ensure_branding_assets()
    _fav = favicon_abs_path()
    st.set_page_config(
        page_title="ai store review analysis",
        layout="wide",
        initial_sidebar_state="collapsed",
        page_icon=_fav if _fav else None,
    )
    _inject_css()
    _inject_file_uploader_labels_once()
    render_masthead(on_about=False)

    env_settings = Settings.from_env()
    gk, gqk, ok = resolve_api_keys(
        env_settings.gemini_api_key,
        env_settings.groq_api_key,
        env_settings.openai_api_key,
        _secrets_get,
    )
    rich = RichAnalyzer(gemini_key=gk, groq_key=gqk, openai_key=ok)
    has_llm_keys = bool(gk or gqk or ok)

    if "analysis_rows" not in st.session_state:
        st.session_state.analysis_rows = []
    _init_split_pools()

    src = _session_main_data_source()

    if src == "Mağaza":
        render_store_link_tab()
    elif src == "Dosya":
        fu_key = f"main_file_uploader_{st.session_state._file_uploader_gen}"
        up = st.file_uploader(t("file.upload_label"), type=["csv", "xlsx"], key=fu_key)
        if up is not None:
            try:
                raw = up.getvalue()
                sig = (up.name, len(raw))
                if st.session_state.get("_file_pool_sig") != sig:
                    if up.name.lower().endswith(".csv"):
                        df = pd.read_csv(io.BytesIO(raw))
                    else:
                        df = pd.read_excel(io.BytesIO(raw))
                    new_rows = load_reviews_from_dataframe(df)
                    existing = list(st.session_state.get("review_pool_file") or [])
                    st.session_state.review_pool_file = dedupe_reviews(existing + new_rows)
                    st.session_state._file_pool_sig = sig
                    srcs = list(st.session_state.get("_file_pool_sources") or [])
                    srcs.append(up.name)
                    st.session_state._file_pool_sources = srcs
                    st.session_state.analysis_rows = []
            except Exception as e:
                st.error(str(e))
        elif st.session_state.review_pool_file:
            srcs = st.session_state.get("_file_pool_sources") or []
            n = len(st.session_state.review_pool_file)
            if len(srcs) > 1:
                shown = ", ".join(srcs[-5:])
                more = "…" if len(srcs) > 5 else ""
                st.caption(
                    t("file.loaded_merged", count=len(srcs), files=shown, more=more, n=n)
                )
            else:
                fn = srcs[0] if srcs else (
                    st.session_state.get("_file_pool_sig", ("—",))[0]
                    if isinstance(st.session_state.get("_file_pool_sig"), tuple)
                    else "—"
                )
                st.caption(t("file.loaded_single", file=fn, n=n))
        if st.session_state.review_pool_file and st.button(
            t("file.clear_pool"), use_container_width=True, key="btn_clear_file_pool"
        ):
            st.session_state.review_pool_file = []
            st.session_state.pop("_file_pool_sig", None)
            st.session_state._file_pool_sources = []
            st.session_state.analysis_rows = []
            st.session_state._file_uploader_gen = int(st.session_state._file_uploader_gen) + 1
            st.rerun()
    elif src == "Metin":
        ta = st.text_area(
            t("paste.label"),
            height=200,
            key="paste_reviews",
            label_visibility="visible",
            placeholder=t("paste.placeholder"),
        )
        if st.button(t("paste.upload_btn"), use_container_width=True, key="btn_paste"):
            lines = [ln.strip() for ln in ta.splitlines() if ln.strip()]
            pool = []
            j = 0
            for ln in lines:
                if not is_valid_comment(ln):
                    continue
                pool.append(
                    {
                        "id": f"paste-{j}",
                        "text": ln,
                        "date": None,
                        "rating": "",
                        "lang": "paste",
                        "is_valid": True,
                    }
                )
                j += 1
            st.session_state.review_pool_paste = pool
            st.session_state.analysis_rows = []
    else:
        render_compare_tab(
            rich=rich,
            has_llm_keys=has_llm_keys,
            default_models=DEFAULT_MODELS,
        )

    pool = _active_review_pool()
    src_cur = _session_main_data_source()
    _is_compare_src_early = src_cur == "Uygulama karşılaştır"
    if _is_compare_src_early:
        # Compare panel kendi "havuzdaki yorum" özetini (uygulama başına ayrı) gösteriyor.
        pool_display_count = 0
    else:
        pool_display_count = len(pool)
    if (not _is_compare_src_early) and _havuz_metric_visible(src_cur, pool_display_count):
        st.markdown(
            f'<div class="metric-strip"><div class="metric-strip-label">{t("metric.pool_count")}</div>'
            f'<div class="metric-strip-value">{pool_display_count}</div></div>',
            unsafe_allow_html=True,
        )
    if (not _is_compare_src_early) and pool:
        raw_df = pd.DataFrame(pool)
        with st.expander(t("download.raw_section"), expanded=False):
            c1, c2, c3 = st.columns(3)
            with c1:
                st.download_button(
                    t("download.csv"),
                    data=df_to_csv_bytes(raw_df),
                    file_name=f"reviews_raw_{datetime.now():%Y%m%d_%H%M}.csv",
                    mime="text/csv",
                    use_container_width=True,
                )
            with c2:
                st.download_button(
                    t("download.excel"),
                    data=df_to_excel_bytes(raw_df),
                    file_name=f"reviews_raw_{datetime.now():%Y%m%d_%H%M}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True,
                )
            with c3:
                try:
                    _raw_pdf = build_raw_pool_pdf_bytes(
                        raw_df.to_dict("records"),
                        source_label=src_cur,
                    )
                    st.download_button(
                        t("download.pdf"),
                        data=_raw_pdf,
                        file_name=safe_pdf_filename(f"yorum_havuzu_{src_cur}"),
                        mime="application/pdf",
                        use_container_width=True,
                    )
                except FileNotFoundError as e:
                    st.caption(str(e))
                except Exception as e:
                    st.caption(f"PDF: {e}")

    _is_compare_src = src_cur == "Uygulama karşılaştır"

    # Compare kaynağında "Analiz ayarları" ve "Duygu analizini başlat" butonu
    # compare panel içinde kendi akışı olarak render edilir — burada gösterilmez.
    if not _is_compare_src:
        st.markdown(
            f'<p class="section-title">{t("section.analysis_settings")}</p>',
            unsafe_allow_html=True,
        )

        _method_labels_main = {
            "Hızlı (heuristic)": t("compare.method_fast"),
            "Zengin (LLM)": t("compare.method_rich"),
        }
        method_pick = st.segmented_control(
            t("section.analysis_settings"),
            options=["Hızlı (heuristic)", "Zengin (LLM)"],
            format_func=lambda v: _method_labels_main.get(v, v),
            selection_mode="single",
            default="Hızlı (heuristic)",
            key="main_analysis_method",
            label_visibility="collapsed",
            width="stretch",
        )
        method = method_pick if method_pick is not None else st.session_state.get(
            "main_analysis_method", "Hızlı (heuristic)"
        )
        use_fast = method == "Hızlı (heuristic)"
        depth = "Standart"
        if not use_fast:
            _depth_labels_main = {
                "Standart": t("compare.depth_std"),
                "Gelişmiş": t("compare.depth_adv"),
            }
            depth = st.radio(
                t("compare.depth_label"),
                ["Standart", "Gelişmiş"],
                horizontal=True,
                key="main_depth",
                format_func=lambda v: _depth_labels_main.get(v, v),
            )
    else:
        method = st.session_state.get("main_analysis_method", "Hızlı (heuristic)") or "Hızlı (heuristic)"
        use_fast = method == "Hızlı (heuristic)"
        depth = st.session_state.get("main_depth", "Standart") or "Standart"

    # Zengin analiz: önce Gemini, kota / hata olursa RichAnalyzer zincirinde Groq → OpenAI.
    provider = "Google Gemini"
    model = DEFAULT_MODELS["Google Gemini"]

    mode_idx = 0 if depth == "Standart" else 1

    if (not _is_compare_src) and st.button(
        t("analysis.start"), type="primary", use_container_width=True
    ):
        prepared = _prepare_pool(pool)
        if not prepared:
            st.warning(t("analysis.warn_load_first"))
        elif not use_fast and not (gk or gqk or ok):
            st.error(t("analysis.err_need_api"))
        else:
            with st.spinner(t("analysis.spinner")):
                bar = st.progress(0.0)
                status = st.empty()

                def prog(done: int, total: int):
                    bar.progress(done / max(total, 1))
                    status.text(f"{done} / {total}")

                rows = analyze_batch(
                    prepared,
                    use_heuristic_only=use_fast,
                    analysis_mode=mode_idx,
                    rich=None if use_fast else rich,
                    provider=provider,
                    model=model.strip() or DEFAULT_MODELS[provider],
                    max_workers=28 if use_fast else 12,
                    progress=prog,
                    max_rich_items=500,
                )
                st.session_state.analysis_rows = rows
                st.session_state._last_analysis_use_fast = use_fast
                bar.empty()
                status.empty()

    rows = st.session_state.analysis_rows
    if rows:
        use_fast_last = bool(st.session_state.get("_last_analysis_use_fast", True))
        render_analysis_results_dashboard(rows, use_fast=use_fast_last)
        df = pd.DataFrame(rows)

        st.markdown(
            f'<p class="section-title section-title--tight">{t("section.reviews")}</p>',
            unsafe_allow_html=True,
        )
        render_analyzed_review_cards(rows, key_prefix="main_analiz")

        out_df = df.drop(columns=["Tarih"], errors="ignore") if "Tarih" in df.columns else df
        d_csv, d_pdf = st.columns(2)
        with d_csv:
            st.download_button(
                t("download.analysis_csv"),
                data=df_to_csv_bytes(out_df),
                file_name=f"analiz_{datetime.now():%Y%m%d_%H%M}.csv",
                mime="text/csv",
                use_container_width=True,
            )
        with d_pdf:
            try:
                _analiz_pdf = build_analysis_pdf_bytes(rows, source_label=src_cur)
                st.download_button(
                    t("download.analysis_pdf"),
                    data=_analiz_pdf,
                    file_name=safe_pdf_filename(f"analiz_{src_cur}"),
                    mime="application/pdf",
                    use_container_width=True,
                )
            except FileNotFoundError as e:
                st.caption(str(e))
            except Exception as e:
                st.caption(f"PDF: {e}")

    render_footer(on_about=False)


if __name__ == "__main__":
    main()
