"""
Store Review Sentiment — capstone entry (Streamlit).

Run from project root:
  streamlit run streamlit_app.py
"""

from __future__ import annotations

import io
import sys
from datetime import datetime
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dotenv import load_dotenv

load_dotenv(ROOT / ".env", override=True)

from store_review.config.settings import Settings
from store_review.config.theme import APP_CSS
from store_review.core.ai_providers import DEFAULT_MODELS, RichAnalyzer, resolve_api_keys
from store_review.core.analyzer import analyze_batch, dedupe_reviews
from store_review.fetchers.file_loader import load_reviews_from_dataframe
from store_review.ui.compare_panel import render_compare_tab
from store_review.ui.store_link_panel import render_store_link_tab
from store_review.utils.exporters import df_to_csv_bytes, df_to_excel_bytes
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


def _inject_css():
    st.markdown(f"<style>{APP_CSS}</style>", unsafe_allow_html=True)


SOURCE_OPTIONS = [
    "Mağaza (ara / link)",
    "Dosya yükle",
    "Metin yapıştır",
    "Karşılaştır",
]
SOURCE_POOL_KEY = {
    "Mağaza (ara / link)": "store",
    "Dosya yükle": "file",
    "Metin yapıştır": "paste",
    "Karşılaştır": "compare",
}


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
    label = st.session_state.get("main_data_source_tab") or SOURCE_OPTIONS[0]
    pk = SOURCE_POOL_KEY.get(label, "store")
    if pk == "compare":
        return []
    return list(st.session_state.get(f"review_pool_{pk}") or [])


def _on_data_source_change() -> None:
    st.session_state.analysis_rows = []


def main():
    st.set_page_config(
        page_title="AI Mağaza Yorumu Analizi",
        layout="centered",
        initial_sidebar_state="collapsed",
    )
    _inject_css()

    st.markdown(
        """
<div class="hero-full-bleed">
  <div class="hero-card">
    <h1 class="hero-title">AI Mağaza Yorumu Analizi</h1>
  </div>
</div>
""",
        unsafe_allow_html=True,
    )

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

    st.markdown('<p class="source-section-title">Veri kaynağı</p>', unsafe_allow_html=True)
    st.radio(
        "",
        SOURCE_OPTIONS,
        horizontal=True,
        label_visibility="collapsed",
        key="main_data_source_tab",
        on_change=_on_data_source_change,
    )

    src = st.session_state.get("main_data_source_tab") or SOURCE_OPTIONS[0]

    if src == "Mağaza (ara / link)":
        render_store_link_tab()
    elif src == "Dosya yükle":
        st.caption("CSV veya Excel; metin sütunu otomatik eşlenir (ör. Yorum, review, text).")
        fu_key = f"main_file_uploader_{st.session_state._file_uploader_gen}"
        up = st.file_uploader("Dosya seç", type=["csv", "xlsx"], key=fu_key)
        if up is not None:
            try:
                raw = up.getvalue()
                sig = (up.name, len(raw))
                if st.session_state.get("_file_pool_sig") != sig:
                    if up.name.lower().endswith(".csv"):
                        df = pd.read_csv(io.BytesIO(raw))
                    else:
                        df = pd.read_excel(io.BytesIO(raw))
                    st.session_state.review_pool_file = load_reviews_from_dataframe(df)
                    st.session_state._file_pool_sig = sig
                    st.session_state.analysis_rows = []
                    st.success(
                        f"{len(st.session_state.review_pool_file)} satır yüklendi (filtre sonrası)."
                    )
            except Exception as e:
                st.error(str(e))
        elif st.session_state.review_pool_file:
            sig = st.session_state.get("_file_pool_sig")
            fn = sig[0] if isinstance(sig, tuple) and sig else "—"
            st.caption(
                f"Son yüklenen dosya havuzunda: **{fn}** "
                f"({len(st.session_state.review_pool_file)} yorum). Yeni dosya seçebilirsiniz."
            )
        if st.session_state.review_pool_file and st.button(
            "Dosya havuzunu temizle", use_container_width=True, key="btn_clear_file_pool"
        ):
            st.session_state.review_pool_file = []
            st.session_state.pop("_file_pool_sig", None)
            st.session_state.analysis_rows = []
            st.session_state._file_uploader_gen = int(st.session_state._file_uploader_gen) + 1
            st.rerun()
    elif src == "Metin yapıştır":
        st.caption("Her satır bir kullanıcı yorumu olacak şekilde yapıştırın.")
        ta = st.text_area(
            "Yorumlar",
            height=200,
            key="paste_reviews",
            label_visibility="visible",
            placeholder="Örn: Uygulama çok iyi ama bildirimler bazen geç geliyor.\nHer satıra bir yorum…",
        )
        if st.button("Metni havuza yükle", use_container_width=True, key="btn_paste"):
            lines = [ln.strip() for ln in ta.splitlines() if ln.strip()]
            pool = []
            for i, ln in enumerate(lines):
                if not is_valid_comment(ln):
                    continue
                pool.append(
                    {
                        "id": f"paste-{i}",
                        "text": ln,
                        "date": None,
                        "rating": "",
                        "lang": "paste",
                        "is_valid": True,
                    }
                )
            st.session_state.review_pool_paste = pool
            st.success(f"{len(pool)} yorum hazır.")
            st.session_state.analysis_rows = []
    else:
        render_compare_tab(
            rich=rich,
            has_llm_keys=has_llm_keys,
            default_models=DEFAULT_MODELS,
        )

    st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)

    pool = _active_review_pool()
    st.markdown(
        f'<div class="metric-strip"><div class="metric-strip-label">Havuzdaki yorum</div>'
        f'<div class="metric-strip-value">{len(pool)}</div></div>',
        unsafe_allow_html=True,
    )

    if pool:
        raw_df = pd.DataFrame(pool)
        with st.expander("Ham veriyi indir (analiz öncesi)", expanded=False):
            c1, c2 = st.columns(2)
            with c1:
                st.download_button(
                    "CSV indir",
                    data=df_to_csv_bytes(raw_df),
                    file_name=f"reviews_raw_{datetime.now():%Y%m%d_%H%M}.csv",
                    mime="text/csv",
                    use_container_width=True,
                )
            with c2:
                st.download_button(
                    "Excel indir",
                    data=df_to_excel_bytes(raw_df),
                    file_name=f"reviews_raw_{datetime.now():%Y%m%d_%H%M}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True,
                )

    st.markdown('<p class="section-title">Analiz ayarları</p>', unsafe_allow_html=True)

    method = st.radio(
        "",
        ["Hızlı (heuristic)", "Zengin (LLM)"],
        horizontal=True,
        label_visibility="collapsed",
        key="main_analysis_method",
    )

    use_fast = method == "Hızlı (heuristic)"
    col_d, col_p = st.columns(2)
    with col_d:
        depth = st.radio(
            "Derinlik (yalnız zengin)",
            ["Standart", "Gelişmiş"],
            horizontal=True,
            disabled=use_fast,
        )
    with col_p:
        provider = st.selectbox(
            "Öncelikli sağlayıcı",
            ["Google Gemini", "Groq AI", "OpenAI"],
            disabled=use_fast,
        )

    model = st.text_input(
        "Model adı",
        value=DEFAULT_MODELS.get(provider, ""),
        disabled=use_fast,
        help="Boş bırakırsanız sağlayıcı varsayılanı kullanılır.",
    )

    mode_idx = 0 if depth == "Standart" else 1

    if st.button("Duygu analizini başlat", type="primary", use_container_width=True):
        prepared = _prepare_pool(pool)
        if not prepared:
            st.warning("Önce yorum yükleyin.")
        elif not use_fast and not (gk or gqk or ok):
            st.error("Zengin analiz için en az bir API anahtarı gerekir.")
        else:
            with st.spinner("Yorumlar analiz ediliyor…"):
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
                bar.empty()
                status.empty()
            st.divider()

    rows = st.session_state.analysis_rows
    if rows:
        st.divider()
        st.markdown('<p class="section-title">Sonuçlar</p>', unsafe_allow_html=True)
        df = pd.DataFrame(rows)
        vc = df["Baskın Duygu"].value_counts()
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Toplam", len(df))
        for col, label in [(m2, "Olumlu"), (m3, "Olumsuz"), (m4, "İstek/Görüş")]:
            col.metric(label, int(vc.get(label, 0)))

        pie_df = vc.reset_index()
        pie_df.columns = ["duygu", "adet"]
        fig = px.pie(
            pie_df,
            names="duygu",
            values="adet",
            hole=0.45,
            color="duygu",
            color_discrete_map={
                "Olumlu": "#34D399",
                "Olumsuz": "#F87171",
                "İstek/Görüş": "#60A5FA",
                "—": "#94A3B8",
            },
        )
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#334155"),
        )
        st.plotly_chart(fig, use_container_width=True)

        st.dataframe(df, use_container_width=True, height=420)

        out_df = df.drop(columns=["Tarih"], errors="ignore") if "Tarih" in df.columns else df
        st.download_button(
            "Sonuçları CSV indir",
            data=df_to_csv_bytes(out_df),
            file_name=f"analiz_{datetime.now():%Y%m%d_%H%M}.csv",
            mime="text/csv",
            use_container_width=True,
        )


if __name__ == "__main__":
    main()
