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
[data-testid="stVerticalBlock"].st-key-cmp_shell [data-testid="stSelectbox"] [data-testid="stWidgetLabel"],
[data-testid="stVerticalBlockBorderWrapper"].st-key-cmp_shell [data-testid="stSelectbox"] [data-testid="stWidgetLabel"] {
  display: none !important;
  height: 0 !important;
  min-height: 0 !important;
  margin: 0 !important;
  padding: 0 !important;
  overflow: hidden !important;
}
[data-testid="stVerticalBlock"].st-key-cmp_shell [data-testid="stSelectbox"],
[data-testid="stVerticalBlockBorderWrapper"].st-key-cmp_shell [data-testid="stSelectbox"] {
  margin-top: 0 !important;
  margin-bottom: 0 !important;
}
[data-testid="stVerticalBlock"].st-key-cmp_shell .cmp-selected-summary,
[data-testid="stVerticalBlockBorderWrapper"].st-key-cmp_shell .cmp-selected-summary {
  margin-top: -4px !important;
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
[data-testid="stVerticalBlock"].st-key-cmp_shell [data-testid="column"],
[data-testid="stVerticalBlockBorderWrapper"].st-key-cmp_shell [data-testid="column"] {
  min-width: 0 !important;
}
[data-testid="stVerticalBlock"].st-key-cmp_shell [data-testid="stHorizontalBlock"],
[data-testid="stVerticalBlockBorderWrapper"].st-key-cmp_shell [data-testid="stHorizontalBlock"] {
  gap: 0.35rem !important;
}
[data-testid="stVerticalBlock"].st-key-cmp_shell [data-baseweb="segmented-control"],
[data-testid="stVerticalBlockBorderWrapper"].st-key-cmp_shell [data-baseweb="segmented-control"] {
  width: 100% !important;
  max-width: 100% !important;
}
[data-testid="stVerticalBlock"].st-key-cmp_shell [data-baseweb="segmented-control"] button,
[data-testid="stVerticalBlockBorderWrapper"].st-key-cmp_shell [data-baseweb="segmented-control"] button {
  flex: 1 1 0 !important;
  min-width: 0 !important;
}
[data-testid="stVerticalBlock"].st-key-cmp_plat_row_0 .sl-plat-radio-wrap,
[data-testid="stVerticalBlock"].st-key-cmp_plat_row_1 .sl-plat-radio-wrap,
[data-testid="stVerticalBlockBorderWrapper"].st-key-cmp_plat_row_0 .sl-plat-radio-wrap,
[data-testid="stVerticalBlockBorderWrapper"].st-key-cmp_plat_row_1 .sl-plat-radio-wrap {
  margin-top: 2px !important;
  margin-bottom: 2px !important;
}
[data-testid="stVerticalBlock"].st-key-cmp_plat_row_0 [data-testid="stHorizontalBlock"] > [data-testid="column"]:last-child,
[data-testid="stVerticalBlock"].st-key-cmp_plat_row_1 [data-testid="stHorizontalBlock"] > [data-testid="column"]:last-child,
[data-testid="stVerticalBlockBorderWrapper"].st-key-cmp_plat_row_0 [data-testid="stHorizontalBlock"] > [data-testid="column"]:last-child,
[data-testid="stVerticalBlockBorderWrapper"].st-key-cmp_plat_row_1 [data-testid="stHorizontalBlock"] > [data-testid="column"]:last-child,
[data-testid="stVerticalBlock"].st-key-cmp_reset_row_0 [data-testid="stHorizontalBlock"] > [data-testid="column"]:last-child,
[data-testid="stVerticalBlock"].st-key-cmp_reset_row_1 [data-testid="stHorizontalBlock"] > [data-testid="column"]:last-child,
[data-testid="stVerticalBlockBorderWrapper"].st-key-cmp_reset_row_0 [data-testid="stHorizontalBlock"] > [data-testid="column"]:last-child,
[data-testid="stVerticalBlockBorderWrapper"].st-key-cmp_reset_row_1 [data-testid="stHorizontalBlock"] > [data-testid="column"]:last-child {
  display: flex !important;
  justify-content: flex-end !important;
  align-items: center !important;
  align-self: center !important;
}
[data-testid="stVerticalBlock"].st-key-cmp_plat_row_0 [data-testid="stHorizontalBlock"] > [data-testid="column"]:last-child .stButton,
[data-testid="stVerticalBlock"].st-key-cmp_plat_row_1 [data-testid="stHorizontalBlock"] > [data-testid="column"]:last-child .stButton,
[data-testid="stVerticalBlockBorderWrapper"].st-key-cmp_plat_row_0 [data-testid="stHorizontalBlock"] > [data-testid="column"]:last-child .stButton,
[data-testid="stVerticalBlockBorderWrapper"].st-key-cmp_plat_row_1 [data-testid="stHorizontalBlock"] > [data-testid="column"]:last-child .stButton,
[data-testid="stVerticalBlock"].st-key-cmp_reset_row_0 [data-testid="stHorizontalBlock"] > [data-testid="column"]:last-child .stButton,
[data-testid="stVerticalBlock"].st-key-cmp_reset_row_1 [data-testid="stHorizontalBlock"] > [data-testid="column"]:last-child .stButton,
[data-testid="stVerticalBlockBorderWrapper"].st-key-cmp_reset_row_0 [data-testid="stHorizontalBlock"] > [data-testid="column"]:last-child .stButton,
[data-testid="stVerticalBlockBorderWrapper"].st-key-cmp_reset_row_1 [data-testid="stHorizontalBlock"] > [data-testid="column"]:last-child .stButton {
  width: auto !important;
}
[data-testid="stVerticalBlock"].st-key-cmp_plat_row_0 [data-testid="stHorizontalBlock"] > [data-testid="column"]:last-child .stButton > button,
[data-testid="stVerticalBlock"].st-key-cmp_plat_row_1 [data-testid="stHorizontalBlock"] > [data-testid="column"]:last-child .stButton > button,
[data-testid="stVerticalBlockBorderWrapper"].st-key-cmp_plat_row_0 [data-testid="stHorizontalBlock"] > [data-testid="column"]:last-child .stButton > button,
[data-testid="stVerticalBlockBorderWrapper"].st-key-cmp_plat_row_1 [data-testid="stHorizontalBlock"] > [data-testid="column"]:last-child .stButton > button,
[data-testid="stVerticalBlock"].st-key-cmp_reset_row_0 [data-testid="stHorizontalBlock"] > [data-testid="column"]:last-child .stButton > button,
[data-testid="stVerticalBlock"].st-key-cmp_reset_row_1 [data-testid="stHorizontalBlock"] > [data-testid="column"]:last-child .stButton > button,
[data-testid="stVerticalBlockBorderWrapper"].st-key-cmp_reset_row_0 [data-testid="stHorizontalBlock"] > [data-testid="column"]:last-child .stButton > button,
[data-testid="stVerticalBlockBorderWrapper"].st-key-cmp_reset_row_1 [data-testid="stHorizontalBlock"] > [data-testid="column"]:last-child .stButton > button {
  width: auto !important;
  min-width: 5.5rem !important;
}
[data-testid="stVerticalBlock"].st-key-cmp_date_method_row [data-testid="stHorizontalBlock"] > [data-testid="column"]:first-child,
[data-testid="stVerticalBlockBorderWrapper"].st-key-cmp_date_method_row [data-testid="stHorizontalBlock"] > [data-testid="column"]:first-child {
  display: flex !important;
  justify-content: flex-start !important;
  align-items: center !important;
}
[data-testid="stVerticalBlock"].st-key-cmp_date_method_row [data-testid="stHorizontalBlock"] > [data-testid="column"]:last-child,
[data-testid="stVerticalBlockBorderWrapper"].st-key-cmp_date_method_row [data-testid="stHorizontalBlock"] > [data-testid="column"]:last-child {
  display: flex !important;
  justify-content: flex-end !important;
  align-items: center !important;
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


def _cmp_review_chip_label(meta_by_slug: dict[str, Any], slug: str, letter: str, *, max_len: int = 30) -> str:
    t = str((meta_by_slug.get(slug) or {}).get("title") or slug).strip()
    if len(t) > max_len:
        t = t[: max_len - 1] + "…"
    return f"{letter} · {t}"


def _cmp_pick_prefix(slot: int) -> str:
    return f"cmp_pick_{slot}_"


def _init_cmp_pick_defaults(slot: int) -> None:
    p = _cmp_pick_prefix(slot)
    pairs: list[tuple[str, Any]] = [
        ("selected_id", None),
        ("selected_platform", None),
        ("selected_title", ""),
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
    st.session_state[f"{p}selected_title"] = ""
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
            st.session_state[f"{p}selected_title"] = ""

    resolved, resolve_msg = resolve_direct_input(text)
    if resolve_msg:
        st.info(resolve_msg)

    is_selected = st.session_state.get(f"{p}selected_id") is not None

    if not text and not is_selected:
        st.session_state[f"{p}search_results"] = []
        st.session_state[f"{p}last_query"] = ""

    if looks_like_search_keyword(text):
        st.session_state[f"{p}search_performed"] = True

    sid = st.session_state.get(f"{p}selected_id")
    splat = st.session_state.get(f"{p}selected_platform")

    if st.session_state.get(f"{p}search_performed"):

        def _cmp_plat_changed() -> None:
            st.session_state[f"{p}last_query"] = ""

        with st.container(key=f"cmp_plat_row_{slot}"):
            plat_c, reset_c = st.columns([4, 1], gap="small", vertical_alignment="center")
            with plat_c:
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
            with reset_c:
                if sid and st.button("Sıfırla", key=f"cmp_slot_reset_{slot}", use_container_width=False):
                    _reset_cmp_slot(slot)
                    st.rerun()

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
                            st.session_state[f"{p}selected_title"] = str(app.get("title") or "")[:120]
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
    elif sid:
        with st.container(key=f"cmp_reset_row_{slot}"):
            _, reset_c = st.columns([4, 1], gap="small", vertical_alignment="center")
            with reset_c:
                if st.button("Sıfırla", key=f"cmp_slot_reset_{slot}", use_container_width=False):
                    _reset_cmp_slot(slot)
                    st.rerun()

    sid = st.session_state.get(f"{p}selected_id")
    splat = st.session_state.get(f"{p}selected_platform")
    if sid:
        stitle = (st.session_state.get(f"{p}selected_title") or "").strip()
        if stitle:
            st.markdown(
                '<div class="cmp-selected-summary">'
                f'<p style="margin:0;font-size:0.88rem;color:#0f172a;line-height:1.3;"><b>{html.escape(stitle)}</b></p>'
                f'<p style="margin:2px 0 0 0;font-size:0.75rem;color:#64748b;line-height:1.25;word-break:break-all;">'
                f'<code style="font-size:0.72rem;">{html.escape(str(sid))}</code> · '
                f"<b>{html.escape(str(splat or '—'))}</b></p>"
                "</div>",
                unsafe_allow_html=True,
            )
        else:
            sid_e = html.escape(str(sid))
            sp_e = html.escape(str(splat or "—"))
            st.markdown(
                '<div class="cmp-selected-summary">'
                f'<p style="margin:0;font-size:0.82rem;color:#64748b;">Seçili: <code>{sid_e}</code> · <b>{sp_e}</b></p>'
                "</div>",
                unsafe_allow_html=True,
            )


def merge_compare_details_for_dashboard() -> list[dict[str, Any]]:
    """cmp_detail_rows + cmp_results → ana ekran analiz tablosu (Uygulama sütunu)."""
    detail_cmp = st.session_state.get("cmp_detail_rows") or {}
    meta_cmp = st.session_state.get("cmp_results") or {}
    merged: list[dict[str, Any]] = []
    n = 1
    for slug, app_rows in detail_cmp.items():
        title = (meta_cmp.get(slug) or {}).get("title", slug)
        for r in app_rows:
            row = dict(r)
            row["No"] = n
            n += 1
            row["Uygulama"] = title
            merged.append(row)
    return merged


def execute_compare_analysis(
    *,
    rich: RichAnalyzer,
    has_llm_keys: bool,
    default_models: dict[str, str],
    use_heuristic_only: bool,
    analysis_mode: int,
) -> tuple[int, list[str]]:
    """
    İki slot için mağazadan yorum çekip analiz eder; cmp_results / cmp_detail_rows güncellenir.
    Dönüş: (tamamlanan uygulama sayısı 0–2, hata metinleri).
    """
    provider = "Google Gemini"
    model = (default_models.get("Google Gemini") or "").strip() or default_models.get(provider, "")

    time_label = st.session_state.get("cmp_time_range") or RANGE_OPTIONS[1]
    if time_label not in RANGE_DAYS:
        time_label = RANGE_OPTIONS[1]
    days = RANGE_DAYS[time_label]

    inputs = [_cmp_slot_effective_raw(0), _cmp_slot_effective_raw(1)]
    if sum(1 for x in inputs if x) < 2:
        return 0, ["İki uygulama için de paket, App Store ID veya mağaza linki / seçim gerekir."]
    if not use_heuristic_only and not has_llm_keys:
        return 0, ["Zengin analiz için en az bir API anahtarı gerekir."]

    def _resolve_one(raw: str) -> tuple[Optional[ResolvedApp], Optional[str]]:
        s = (raw or "").strip()
        if not s:
            return None, None
        return resolve_direct_input(s)

    results: dict[str, dict[str, Any]] = {}
    detail_rows: dict[str, list[dict]] = {}
    errors: list[str] = []

    for raw in inputs:
        resolved, msg = _resolve_one(raw)
        if msg:
            st.info(str(msg))
        if resolved is None:
            errors.append(f"Çözülemedi: `{raw[:48]}…`" if len(raw) > 48 else f"Çözülemedi: `{raw}`")
            continue

        meta = _metadata(resolved)
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

            prep_n = len(prepared)
            pool_n = len(pool)
            rows = analyze_batch(
                prepared,
                use_heuristic_only=use_heuristic_only,
                analysis_mode=analysis_mode,
                rich=None if use_heuristic_only else rich,
                provider=provider,
                model=model,
                max_workers=28 if use_heuristic_only else 12,
                progress=None,
                max_rich_items=500,
            )
            agg = _aggregate_rows(rows)
            slug = f"{resolved.platform}:{resolved.app_id}"
            detail_rows[slug] = list(rows)
            rich_cap = (not use_heuristic_only) and (prep_n > 500)
            results[slug] = {
                **meta,
                **agg,
                "app_id": resolved.app_id,
                "platform": resolved.platform,
                "chart_label": f"{meta['title'][:36]}{'…' if len(meta['title']) > 36 else ''} ({'Play' if resolved.platform == 'android' else 'App Store'})",
                "cmp_pool_fetched": pool_n,
                "cmp_pool_prepared": prep_n,
                "cmp_rich_capped": rich_cap,
                "cmp_rich_cap_limit": 500 if rich_cap else None,
            }
        except Exception as e:
            errors.append(f"{meta.get('title', raw)}: {e}")

    st.session_state.cmp_results = results
    st.session_state.cmp_detail_rows = detail_rows
    st.session_state.cmp_range_label = time_label
    st.session_state.cmp_days_used = int(days)
    return len(results), errors


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
        ca, cb = st.columns(2, gap="small")
        with ca:
            _render_compare_app_picker(0, "Uygulama 1")
        with cb:
            _render_compare_app_picker(1, "Uygulama 2")

        with st.container(key="cmp_date_method_row"):
            tcol, mid, mcol = st.columns([1, 0.2, 1.15], gap="medium", vertical_alignment="center")
            with tcol:
                time_label = st.selectbox(
                    "Tarih",
                    RANGE_OPTIONS,
                    index=1,
                    key="cmp_time_range",
                    label_visibility="hidden",
                    width="content",
                )
            with mid:
                st.empty()
            with mcol:
                push_l, push_r = st.columns([0.22, 0.78], gap="small", vertical_alignment="center")
                with push_l:
                    st.empty()
                with push_r:
                    mm1, mm2 = st.columns(2, gap="small", vertical_alignment="center")
                    with mm1:
                        cmp_method = st.radio(
                            "Karşılaştırma analiz yöntemi",
                            ["Hızlı (heuristic)", "Zengin (LLM)"],
                            horizontal=True,
                            key="cmp_method",
                            label_visibility="collapsed",
                        )
                    use_fast = cmp_method == "Hızlı (heuristic)"
                    with mm2:
                        if use_fast:
                            mode_idx = 0
                            st.caption("Heuristic: derinlik sabit.")
                        else:
                            depth = st.radio(
                                "Derinlik",
                                ["Standart", "Gelişmiş"],
                                horizontal=True,
                                key="cmp_depth",
                                label_visibility="collapsed",
                            )
                            mode_idx = 0 if depth == "Standart" else 1
        days = RANGE_DAYS[time_label]

        res = st.session_state.get("cmp_results") or {}
        b1, b2 = st.columns([2.2, 1], gap="small")
        with b1:
            if st.button("Karşılaştırmayı başlat", type="primary", use_container_width=True, key="cmp_start"):
                if sum(1 for x in (_cmp_slot_effective_raw(0), _cmp_slot_effective_raw(1)) if x) < 2:
                    st.warning("İki uygulama için de ID veya link girin.")
                elif not use_fast and not has_llm_keys:
                    st.error("Zengin analiz için en az bir API anahtarı gerekir (.env veya Streamlit secrets).")
                else:
                    with st.spinner("Uygulamalar analiz ediliyor…"):
                        n_ok, errs = execute_compare_analysis(
                            rich=rich,
                            has_llm_keys=has_llm_keys,
                            default_models=default_models,
                            use_heuristic_only=use_fast,
                            analysis_mode=mode_idx,
                        )
                    for er in errs:
                        st.error(er)
        with b2:
            if res and st.button("Sonuçları temizle", key="cmp_clear", use_container_width=True):
                st.session_state.cmp_results = {}
                st.session_state.cmp_detail_rows = {}
                st.session_state.pop("cmp_range_label", None)
                st.session_state.pop("cmp_days_used", None)
                st.rerun()

        if res:
            st.markdown("#### Özet")
            days_u = st.session_state.get("cmp_days_used")
            rng_lbl = st.session_state.get("cmp_range_label") or time_label
            if days_u is not None:
                st.markdown(
                    f'<p style="margin:0 0 10px 0;font-size:0.8rem;color:#475569;">'
                    f"{html.escape(str(rng_lbl))} · <b>{int(days_u)}</b> gün</p>",
                    unsafe_allow_html=True,
                )
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
                    rt = data.get("rating")
                    rct = data.get("ratings")
                    if rt is not None or (rct is not None and int(rct or 0) > 0):
                        st.markdown(
                            f'<p style="margin:0 0 4px 0;font-size:0.72rem;color:#64748b;">'
                            f"Mağaza <b>{float(rt or 0):.1f}</b> · <b>{int(rct or 0)}</b> oy</p>",
                            unsafe_allow_html=True,
                        )
                    fe = data.get("cmp_pool_fetched")
                    if fe is not None:
                        pr = int(data.get("cmp_pool_prepared") or 0)
                        cap = bool(data.get("cmp_rich_capped"))
                        lim = data.get("cmp_rich_cap_limit")
                        bits = [f"Ham <b>{int(fe)}</b>", f"Filtre <b>{pr}</b>"]
                        if cap and lim:
                            bits.append(f"LLM ≤<b>{int(lim)}</b>")
                        st.markdown(
                            '<p style="margin:0 0 8px 0;font-size:0.72rem;color:#64748b;line-height:1.4;">'
                            + " · ".join(bits)
                            + "</p>",
                            unsafe_allow_html=True,
                        )
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
            detail = st.session_state.get("cmp_detail_rows") or {}
            if not detail:
                st.markdown(
                    '<p style="color:#64748b;font-size:0.92rem;margin:0;">'
                    "Yorum satırları bulunamadı. Karşılaştırmayı yeniden çalıştırın.</p>",
                    unsafe_allow_html=True,
                )
            else:
                key_list = list(res.keys())[:2]
                if len(key_list) == 1:
                    slug = key_list[0]
                    data = res.get(slug) or {}
                    title = html.escape(str(data.get("title") or slug))
                    rows_d = detail.get(slug) or []
                    st.markdown(
                        f'<p style="font-weight:700;color:#334155;margin:8px 0 4px 0;">{title}</p>',
                        unsafe_allow_html=True,
                    )
                    aid_disp = str(data.get("app_id", "") or "")
                    ch_disp = str(data.get("chart_label", "") or "")
                    st.caption(f"{int(data.get('total', 0))} · {aid_disp} · {ch_disp}")
                    if not rows_d:
                        st.write("—")
                    else:
                        render_analyzed_review_cards(rows_d, key_prefix="cmp_0")
                else:
                    slugs = key_list

                    def _seg_label(s: str) -> str:
                        i = slugs.index(s)
                        return _cmp_review_chip_label(res, s, "A" if i == 0 else "B")

                    pick = st.segmented_control(
                        "Yorumlar",
                        options=slugs,
                        format_func=_seg_label,
                        selection_mode="single",
                        default=slugs[0],
                        key="cmp_review_segment",
                        label_visibility="collapsed",
                        width="stretch",
                    )
                    slug = pick if pick is not None else slugs[0]
                    idx = slugs.index(slug)
                    data = res.get(slug) or {}
                    title = html.escape(str(data.get("title") or slug))
                    rows_d = detail.get(slug) or []
                    st.markdown(
                        f'<p style="font-weight:700;color:#334155;margin:10px 0 4px 0;">{title}</p>',
                        unsafe_allow_html=True,
                    )
                    aid_disp = str(data.get("app_id", "") or "")
                    ch_disp = str(data.get("chart_label", "") or "")
                    st.caption(f"{int(data.get('total', 0))} · {aid_disp} · {ch_disp}")
                    if not rows_d:
                        st.write("—")
                    else:
                        render_analyzed_review_cards(rows_d, key_prefix=f"cmp_{idx}")
