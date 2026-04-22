"""
İki uygulama için mağaza yorumu çekme + duygu özeti (Karşılaştır sekmesi).
"""

from __future__ import annotations

import html
from typing import Any, Optional

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from store_review.core.ai_providers import RichAnalyzer
from store_review.core.analyzer import analyze_batch, dedupe_reviews
from store_review.fetchers.app_discovery import (
    ResolvedApp,
    looks_like_search_keyword,
    resolve_direct_input,
    search_app_store_itunes,
    search_play_store,
)
from store_review.fetchers.app_store import get_app_store_reviews
from store_review.fetchers.google_play import fetch_google_play_reviews
from store_review.ui.review_cards import render_analyzed_review_cards
from store_review.ui.store_link_panel import (
    RANGE_DAYS,
    RANGE_OPTIONS,
    _inject_store_search_css,
)

_CMP_COMPACT_CSS = """
<style>
[data-testid="stVerticalBlock"].st-key-cmp_shell [data-testid="element-container"],
[data-testid="stVerticalBlockBorderWrapper"].st-key-cmp_shell [data-testid="element-container"] {
  margin-top: 0 !important;
  margin-bottom: 0.2rem !important;
}
[data-testid="stVerticalBlock"].st-key-cmp_shell .sl-plat-radio-wrap,
[data-testid="stVerticalBlockBorderWrapper"].st-key-cmp_shell .sl-plat-radio-wrap {
  margin: 4px 0 6px !important;
}
[data-testid="stVerticalBlock"].st-key-cmp_shell hr,
[data-testid="stVerticalBlockBorderWrapper"].st-key-cmp_shell hr {
  display: none !important;
  margin: 0 !important;
  height: 0 !important;
  border: 0 !important;
}
[data-testid="stVerticalBlock"].st-key-cmp_shell [data-testid="stMetricContainer"],
[data-testid="stVerticalBlockBorderWrapper"].st-key-cmp_shell [data-testid="stMetricContainer"] {
  padding-top: 0.1rem !important;
  padding-bottom: 0.1rem !important;
}
[data-testid="stVerticalBlock"].st-key-cmp_shell [data-testid="stPlotlyChart"],
[data-testid="stVerticalBlockBorderWrapper"].st-key-cmp_shell [data-testid="stPlotlyChart"] {
  margin-top: 0.25rem !important;
  margin-bottom: 0.35rem !important;
}
[data-testid="stVerticalBlock"].st-key-cmp_shell [data-testid="stCaption"],
[data-testid="stVerticalBlockBorderWrapper"].st-key-cmp_shell [data-testid="stCaption"] {
  margin-top: 0.1rem !important;
  margin-bottom: 0.15rem !important;
}
[data-testid="stVerticalBlock"].st-key-cmp_shell [data-testid="stHeadingWithActionElements"],
[data-testid="stVerticalBlockBorderWrapper"].st-key-cmp_shell [data-testid="stHeadingWithActionElements"] {
  margin-top: 0.35rem !important;
  margin-bottom: 0.15rem !important;
}
</style>
"""


def _prepare_pool(rows: list[dict]) -> list[dict]:
    from store_review.utils.validators import is_valid_comment

    out: list[dict] = []
    for r in dedupe_reviews(rows):
        t = str(r.get("text", "")).strip()
        if len(t) < 2:
            continue
        rr = dict(r)
        rr["is_valid"] = is_valid_comment(t)
        out.append(rr)
    return out


def _metadata_android(app_id: str) -> dict[str, Any]:
    try:
        from google_play_scraper import app as play_app

        info = play_app(app_id, lang="tr", country="tr")
        cats = info.get("categories") or []
        genre = "—"
        if cats and isinstance(cats[0], dict):
            genre = str(cats[0].get("name", "—"))
        return {
            "title": str(info.get("title") or app_id),
            "icon": str(info.get("icon") or "").strip(),
            "store": "Google Play",
            "rating": round(float(info.get("score") or 0), 1),
            "ratings": int(info.get("ratings") or 0),
            "installs": str(info.get("installs") or "—"),
            "version": str(info.get("version") or "—"),
            "genre": genre,
        }
    except Exception:
        return {
            "title": app_id,
            "icon": "",
            "store": "Google Play",
            "rating": 0.0,
            "ratings": 0,
            "installs": "—",
            "version": "—",
            "genre": "—",
        }


def _metadata_ios(app_id: str) -> dict[str, Any]:
    import requests

    title, icon, rating, ratings, ver, genre = app_id, "", 0.0, 0, "—", "—"
    for cc in ("tr", "us", "gb"):
        try:
            r = requests.get(
                f"https://itunes.apple.com/lookup?id={app_id}&country={cc}",
                timeout=8,
            )
            if r.status_code != 200:
                continue
            data = r.json().get("results") or []
            if not data:
                continue
            a0 = data[0]
            title = str(a0.get("trackCensoredName") or a0.get("trackName") or app_id)
            icon = str(a0.get("artworkUrl512") or a0.get("artworkUrl100") or "").strip()
            rating = round(float(a0.get("averageUserRating") or 0), 1)
            ratings = int(a0.get("userRatingCount") or 0)
            ver = str(a0.get("version") or "—")
            genre = str(a0.get("primaryGenreName") or "—")
            break
        except Exception:
            continue
    return {
        "title": title,
        "icon": icon,
        "store": "App Store",
        "rating": rating,
        "ratings": ratings,
        "installs": "App Store",
        "version": ver,
        "genre": genre,
    }


def _metadata(resolved: ResolvedApp) -> dict[str, Any]:
    if resolved.platform == "android":
        return _metadata_android(resolved.app_id)
    return _metadata_ios(resolved.app_id)


def _aggregate_rows(rows: list[dict]) -> dict[str, int | float]:
    if not rows:
        return {
            "total": 0,
            "pos": 0,
            "neg": 0,
            "neu": 0,
            "pos_pct": 0,
            "neg_pct": 0,
            "neu_pct": 0,
            "score": 0,
        }
    df = pd.DataFrame(rows)
    vc = df["Baskın Duygu"].value_counts() if "Baskın Duygu" in df.columns else pd.Series(dtype=int)
    pos = int(vc.get("Olumlu", 0))
    neg = int(vc.get("Olumsuz", 0))
    neu = int(vc.get("İstek/Görüş", 0))
    total_v = pos + neg + neu
    if total_v < 1:
        total_v = 1
    pos_pct = int(pos * 100 / total_v)
    neg_pct = int(neg * 100 / total_v)
    neu_pct = int(neu * 100 / total_v)
    score = int((pos * 100 + neu * 50) / total_v)
    return {
        "total": len(rows),
        "pos": pos,
        "neg": neg,
        "neu": neu,
        "pos_pct": pos_pct,
        "neg_pct": neg_pct,
        "neu_pct": neu_pct,
        "score": score,
    }


def _cmp_pick_prefix(slot: int) -> str:
    return f"cmp_pick_{slot}_"


def _init_cmp_pick_defaults(slot: int) -> None:
    p = _cmp_pick_prefix(slot)
    pairs: list[tuple[str, Any]] = [
        ("selected_id", None),
        ("selected_platform", None),
        ("search_results", []),
        ("last_query", ""),
        ("last_filter", "Android"),
        ("display_n", 12),
        ("search_performed", False),
        ("prev_filter", ""),
    ]
    for name, val in pairs:
        k = f"{p}{name}"
        if k not in st.session_state:
            st.session_state[k] = val


def _apply_pending_cmp_store_in(slot: int) -> None:
    pk = f"_pending_cmp_store_in_{slot}"
    if pk not in st.session_state:
        return
    val = st.session_state.pop(pk)
    st.session_state[f"cmp_store_in_{slot}"] = val


def _reset_cmp_slot(slot: int) -> None:
    p = _cmp_pick_prefix(slot)
    st.session_state[f"cmp_store_in_{slot}"] = ""
    st.session_state[f"{p}selected_id"] = None
    st.session_state[f"{p}selected_platform"] = None
    st.session_state[f"{p}search_results"] = []
    st.session_state[f"{p}last_query"] = ""
    st.session_state[f"{p}display_n"] = 12
    st.session_state[f"{p}search_performed"] = False
    st.session_state[f"{p}prev_filter"] = ""


def _cmp_slot_effective_raw(slot: int) -> str:
    p = _cmp_pick_prefix(slot)
    sid = st.session_state.get(f"{p}selected_id")
    if sid:
        return str(sid).strip()
    return (st.session_state.get(f"cmp_store_in_{slot}") or "").strip()


def _render_compare_app_picker(slot: int, heading: str) -> None:
    """Mağaza sekmesiyle aynı: isim araması + Android/iOS + sonuç listesi + Seç; paket/ID/link doğrudan."""
    _apply_pending_cmp_store_in(slot)
    _init_cmp_pick_defaults(slot)
    p = _cmp_pick_prefix(slot)
    in_key = f"cmp_store_in_{slot}"

    st.text_input(
        f"{heading} — uygulama ara veya mağaza linki / ID",
        key=in_key,
        placeholder="Örn. trendyol, com.example, App Store ID veya mağaza linki",
        label_visibility="visible",
    )
    text = (st.session_state.get(in_key) or "").strip()

    sel_id = st.session_state.get(f"{p}selected_id")
    # Metin kutusu listeden seçilen paketten farklı olabilir (örn. hâlâ "letgo" yazıyor);
    # arama kelimesi iken seçimi silme — yoksa Karşılaştır yalnızca kelimeye düşer ve çözülemez.
    if sel_id and text and text != str(sel_id):
        direct_res, _ = resolve_direct_input(text)
        if direct_res is not None and str(direct_res.app_id) != str(sel_id):
            st.session_state[f"{p}selected_id"] = None
            st.session_state[f"{p}selected_platform"] = None

    resolved, resolve_msg = resolve_direct_input(text)
    if resolve_msg:
        st.info(resolve_msg)

    is_selected = st.session_state.get(f"{p}selected_id") is not None

    if not text and not is_selected:
        st.session_state[f"{p}search_results"] = []
        st.session_state[f"{p}last_query"] = ""

    if looks_like_search_keyword(text):
        st.session_state[f"{p}search_performed"] = True

    if st.session_state.get(f"{p}search_performed"):

        def _cmp_plat_changed() -> None:
            st.session_state[f"{p}last_query"] = ""

        st.markdown('<div class="sl-plat-radio-wrap">', unsafe_allow_html=True)
        st.radio(
            "Platform",
            ["Android", "iOS"],
            horizontal=True,
            key=f"{p}last_filter",
            label_visibility="collapsed",
            on_change=_cmp_plat_changed,
        )
        st.markdown("</div>", unsafe_allow_html=True)

        filt = st.session_state.get(f"{p}last_filter", "Android")
        if looks_like_search_keyword(text) and len(text) >= 2:
            if text != st.session_state.get(f"{p}last_query") or filt != st.session_state.get(f"{p}prev_filter"):
                combined: list = []
                if filt == "iOS":
                    combined.extend(search_app_store_itunes(text))
                else:
                    combined.extend(search_play_store(text))
                st.session_state[f"{p}search_results"] = combined
                st.session_state[f"{p}last_query"] = text
                st.session_state[f"{p}display_n"] = 12
                st.session_state[f"{p}prev_filter"] = filt

            results = st.session_state.get(f"{p}search_results") or []
            if results:
                st.markdown(
                    f'<p class="sl-results-head">Bulunan uygulamalar ({len(results)})</p>',
                    unsafe_allow_html=True,
                )
                n_show = min(int(st.session_state.get(f"{p}display_n") or 12), len(results))
                for idx, app in enumerate(results[:n_show]):
                    ic, inf, bt = st.columns([0.14, 0.62, 0.24])
                    with ic:
                        icon = app.get("icon") or ""
                        if isinstance(icon, str) and icon.startswith("http"):
                            st.markdown(
                                f'<div class="sl-row-icon"><img src="{html.escape(icon)}" alt=""/></div>',
                                unsafe_allow_html=True,
                            )
                        else:
                            st.markdown('<div class="sl-row-noicon">app</div>', unsafe_allow_html=True)
                    with inf:
                        t_esc = html.escape(str(app.get("title", "—")))
                        id_esc = html.escape(str(app.get("appId", "")))
                        st.markdown(
                            f'<div class="sl-row-title">{t_esc}</div><div class="sl-row-id">{id_esc}</div>',
                            unsafe_allow_html=True,
                        )
                    with bt:
                        aid = app.get("appId", "")
                        plat = app.get("platform", "Android")
                        if st.button("Seç", key=f"cmp_sel_{slot}_{idx}_{aid}", use_container_width=True):
                            st.session_state[f"{p}selected_id"] = aid
                            st.session_state[f"{p}selected_platform"] = plat
                            st.session_state[f"{p}search_results"] = []
                            st.session_state[f"{p}last_query"] = ""
                            st.session_state[f"_pending_cmp_store_in_{slot}"] = aid
                            st.rerun()
                if len(results) > n_show:
                    if st.button("Daha fazla göster", key=f"cmp_more_{slot}"):
                        st.session_state[f"{p}display_n"] = min(
                            int(st.session_state.get(f"{p}display_n") or 12) + 12,
                            len(results),
                        )
                        st.rerun()
            elif len(text) >= 2 and looks_like_search_keyword(text):
                st.warning("Sonuç bulunamadı. Farklı anahtar kelime veya platform deneyin.")

    sid = st.session_state.get(f"{p}selected_id")
    splat = st.session_state.get(f"{p}selected_platform")
    if sid:
        st.caption(f"Seçili: `{sid}` · **{splat or '—'}**")
        if st.button("Bu uygulamayı sıfırla", key=f"cmp_slot_reset_{slot}"):
            _reset_cmp_slot(slot)
            st.rerun()


def render_compare_tab(
    *,
    rich: RichAnalyzer,
    has_llm_keys: bool,
    default_models: dict[str, str],
) -> None:
    if "cmp_results" not in st.session_state:
        st.session_state.cmp_results = {}
    if "cmp_detail_rows" not in st.session_state:
        st.session_state.cmp_detail_rows = {}

    _inject_store_search_css()
    st.markdown(_CMP_COMPACT_CSS, unsafe_allow_html=True)
    with st.container(key="cmp_shell"):
        _render_compare_app_picker(0, "Uygulama 1")
        _render_compare_app_picker(1, "Uygulama 2")

        time_label = st.selectbox("Tarih aralığı", RANGE_OPTIONS, index=1, key="cmp_time_range")
        days = RANGE_DAYS[time_label]

        m1, m2 = st.columns(2)
        with m1:
            cmp_method = st.radio(
                "Karşılaştırma analiz yöntemi",
                ["Hızlı (heuristic)", "Zengin (LLM)"],
                horizontal=True,
                key="cmp_method",
                label_visibility="collapsed",
            )
        use_fast = cmp_method == "Hızlı (heuristic)"
        with m2:
            if use_fast:
                mode_idx = 0
                st.caption("Heuristic için derinlik sabit.")
            else:
                depth = st.radio(
                    "Derinlik",
                    ["Standart", "Gelişmiş"],
                    horizontal=True,
                    key="cmp_depth",
                )
                mode_idx = 0 if depth == "Standart" else 1

        provider = "Google Gemini"
        model = default_models.get("Google Gemini", "")

        def _resolve_one(raw: str) -> tuple[Optional[ResolvedApp], Optional[str]]:
            s = (raw or "").strip()
            if not s:
                return None, None
            return resolve_direct_input(s)

        if st.button("Karşılaştırmayı başlat", type="primary", use_container_width=True, key="cmp_start"):
            inputs = [_cmp_slot_effective_raw(0), _cmp_slot_effective_raw(1)]
            if sum(1 for x in inputs if x) < 2:
                st.warning("İki uygulama için de ID veya link girin.")
            elif not use_fast and not has_llm_keys:
                st.error("Zengin analiz için en az bir API anahtarı gerekir (.env veya Streamlit secrets).")
            else:
                results: dict[str, dict[str, Any]] = {}
                detail_rows: dict[str, list[dict]] = {}
                errors: list[str] = []
                model_final = (model or "").strip() or default_models.get(provider, "")

                for raw in inputs:
                    resolved, msg = _resolve_one(raw)
                    if msg:
                        st.info(msg)
                    if resolved is None:
                        errors.append(f"Çözülemedi: `{raw[:48]}…`" if len(raw) > 48 else f"Çözülemedi: `{raw}`")
                        continue

                    meta = _metadata(resolved)
                    with st.spinner(f"«{meta['title']}» yorumlar çekiliyor ve analiz ediliyor…"):
                        try:
                            if resolved.platform == "android":
                                pool = fetch_google_play_reviews(
                                    resolved.app_id,
                                    days,
                                    _progress_callback=lambda x: None,
                                )
                            else:
                                pool = get_app_store_reviews(
                                    resolved.app_id,
                                    _progress_callback=lambda x: None,
                                    _days_limit=days,
                                )
                            prepared = _prepare_pool(pool)
                            if not prepared:
                                errors.append(f"{meta['title']}: analiz edilecek yorum yok.")
                                continue

                            rows = analyze_batch(
                                prepared,
                                use_heuristic_only=use_fast,
                                analysis_mode=mode_idx,
                                rich=None if use_fast else rich,
                                provider=provider,
                                model=model_final,
                                max_workers=28 if use_fast else 12,
                                progress=None,
                                max_rich_items=500,
                            )
                            agg = _aggregate_rows(rows)
                            slug = f"{resolved.platform}:{resolved.app_id}"
                            detail_rows[slug] = list(rows)
                            results[slug] = {
                                **meta,
                                **agg,
                                "app_id": resolved.app_id,
                                "platform": resolved.platform,
                                "chart_label": f"{meta['title'][:36]}{'…' if len(meta['title']) > 36 else ''} ({'Play' if resolved.platform == 'android' else 'App Store'})",
                            }
                        except Exception as e:
                            errors.append(f"{meta.get('title', raw)}: {e}")

                st.session_state.cmp_results = results
                st.session_state.cmp_detail_rows = detail_rows
                st.session_state.cmp_range_label = time_label
                if errors:
                    for er in errors:
                        st.error(er)
        res = st.session_state.get("cmp_results") or {}
        if res:
            if st.button("Karşılaştırma sonuçlarını temizle", key="cmp_clear"):
                st.session_state.cmp_results = {}
                st.session_state.cmp_detail_rows = {}
                st.session_state.pop("cmp_range_label", None)
                st.rerun()

            st.markdown("#### Özet")
            cols = st.columns(len(res))
            colors = ["#6366F1", "#F97316", "#0EA5E9"]
            for i, (_slug, data) in enumerate(res.items()):
                app_nm = data.get("title") or _slug
                with cols[i]:
                    accent = colors[i % len(colors)]
                    st.markdown(
                        f'<div style="font-size:0.75rem;font-weight:700;color:{accent};margin-bottom:6px;">'
                        f"{html.escape(str(app_nm))}</div>",
                        unsafe_allow_html=True,
                    )
                    icon = (data.get("icon") or "").strip()
                    if icon.startswith("http"):
                        st.image(icon, width=56)
                    st.caption(f"{data.get('store', '')} · {data.get('genre', '—')}")
                    st.metric("Duygu skoru (0–100)", int(data.get("score", 0)))
                    st.metric("Analiz edilen yorum", int(data.get("total", 0)))
                    st.caption(f"Olumlu %{data.get('pos_pct', 0)}")
                    st.progress(min(1.0, max(0.0, int(data.get("pos_pct", 0)) / 100.0)))
                    st.caption(f"Olumsuz %{data.get('neg_pct', 0)}")
                    st.progress(min(1.0, max(0.0, int(data.get("neg_pct", 0)) / 100.0)))
                    st.caption(f"İstek/Görüş %{data.get('neu_pct', 0)}")
                    st.progress(min(1.0, max(0.0, int(data.get("neu_pct", 0)) / 100.0)))

            names = [res[k].get("chart_label") or res[k].get("title") or k for k in res.keys()]
            keys = list(res.keys())
            fig = go.Figure(
                data=[
                    go.Bar(name="Olumlu", x=names, y=[res[k]["pos_pct"] for k in keys], marker_color="#34D399"),
                    go.Bar(name="Olumsuz", x=names, y=[res[k]["neg_pct"] for k in keys], marker_color="#F87171"),
                    go.Bar(
                        name="İstek/Görüş",
                        x=names,
                        y=[res[k]["neu_pct"] for k in keys],
                        marker_color="#60A5FA",
                    ),
                ]
            )
            fig.update_layout(
                barmode="group",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#334155"),
                margin=dict(t=22, b=28),
                yaxis_title="Yüzde",
                height=320,
            )
            st.plotly_chart(fig, use_container_width=True)

            st.markdown("#### Yorumlar")
            range_lbl = st.session_state.get("cmp_range_label") or time_label
            st.caption(f"**{range_lbl}** aralığında analiz edilen yorumlar.")
            detail = st.session_state.get("cmp_detail_rows") or {}
            if not detail:
                st.markdown(
                    '<p style="color:#64748b;font-size:0.92rem;margin:0;">'
                    "Yorum satırları bulunamadı. Karşılaştırmayı yeniden çalıştırın.</p>",
                    unsafe_allow_html=True,
                )
            else:
                key_list = list(res.keys())[:2]
                for idx, slug in enumerate(key_list):
                    data = res.get(slug) or {}
                    title = html.escape(str(data.get("title") or slug))
                    rows_d = detail.get(slug) or []
                    st.markdown(
                        f'<p style="font-weight:700;color:#334155;margin:10px 0 6px 0;">{title}</p>',
                        unsafe_allow_html=True,
                    )
                    st.caption(f"{int(data.get('total', 0))} yorum · {data.get('chart_label', '')}")
                    if not rows_d:
                        st.write("—")
                    else:
                        render_analyzed_review_cards(rows_d, key_prefix=f"cmp_{idx}")
