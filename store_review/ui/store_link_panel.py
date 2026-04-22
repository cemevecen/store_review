"""
Tek mağaza sekmesi: isim araması (Play + App Store), Android/iOS filtresi, sonuçtan seçim, tarih aralığı, çekme.
Eski monolitik streamlit_app "Mağaza Linki" akışının sadeleştirilmiş hali.
"""

from __future__ import annotations

import html

import streamlit as st

from store_review.fetchers.app_discovery import (
    looks_like_search_keyword,
    resolve_direct_input,
    search_app_store_itunes,
    search_play_store,
)
from store_review.fetchers.app_store import get_app_store_reviews
from store_review.fetchers.google_play import fetch_google_play_reviews


def _init_store_state() -> None:
    defaults = {
        "sl_selected_id": None,
        "sl_selected_platform": None,
        "sl_show_search": True,
        "sl_search_results": [],
        "sl_last_query": "",
        "sl_last_filter": "Android",
        "sl_display_n": 12,
        "sl_search_performed": False,
        "_sl_prev_filter": "",
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


def _apply_pending_sl_store_input() -> None:
    """st.text_input(sl_store_input) oluşmadan önce çağrılmalı (Streamlit kuralı)."""
    if "_pending_sl_store_input" not in st.session_state:
        return
    val = st.session_state.pop("_pending_sl_store_input")
    st.session_state["sl_store_input"] = val


def _inject_store_search_css() -> None:
    st.markdown(
        """
<style>
.sl-platform-wrap { display:flex; gap:10px; margin:10px 0 14px; flex-wrap:wrap; }
.sl-platform-wrap button {
  border-radius: 999px !important;
  font-weight: 600 !important;
  border: 2px solid #e2e8f0 !important;
  background: #fff !important;
  color: #0f172a !important;
}
/* Android / iOS — radyo ile seçili durum net */
.sl-plat-radio-wrap { margin: 10px 0 14px; }
.sl-plat-radio-wrap [data-testid="stRadio"] > div { width: 100% !important; }
.sl-plat-radio-wrap [data-testid="stRadio"] div[role="radiogroup"] {
  display: flex !important;
  gap: 12px !important;
  flex-wrap: wrap !important;
}
.sl-plat-radio-wrap [data-testid="stRadio"] div[role="radiogroup"] label {
  flex: 1 1 0 !important;
  min-height: 48px !important;
  margin: 0 !important;
  padding: 12px 18px !important;
  border-radius: 14px !important;
  border: 2px solid #cbd5e1 !important;
  background: #ffffff !important;
  color: #334155 !important;
  font-weight: 600 !important;
  align-items: center !important;
  justify-content: center !important;
  transition: background 0.15s ease, color 0.15s ease, border-color 0.15s ease, box-shadow 0.15s ease !important;
}
.sl-plat-radio-wrap [data-testid="stRadio"] div[role="radiogroup"] label:has(input:checked) {
  background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%) !important;
  color: #ffffff !important;
  border-color: #0f172a !important;
  box-shadow: 0 4px 18px rgba(15, 23, 42, 0.28) !important;
}
.sl-plat-radio-wrap [data-testid="stRadio"] div[role="radiogroup"] label:has(input:checked) p,
.sl-plat-radio-wrap [data-testid="stRadio"] div[role="radiogroup"] label:has(input:checked) span {
  color: #ffffff !important;
}
.sl-results-head {
  font-size:0.82rem; color:#64748b; font-weight:700; text-transform:uppercase;
  letter-spacing:0.06em; margin:6px 0 10px;
}
.sl-row-icon img { width:40px; height:40px; border-radius:50%; object-fit:cover; display:block; }
.sl-row-noicon {
  width:40px; height:40px; border-radius:50%; background:#e2e8f0; color:#64748b;
  display:flex; align-items:center; justify-content:center; font-size:0.62rem;
  font-weight:700; letter-spacing:0.02em;
}
.sl-row-title { font-weight:700; color:#0f172a; font-size:0.9rem; line-height:1.25; }
.sl-row-id { font-size:0.72rem; color:#94a3b8; margin-top:2px; word-break:break-all; }
.sl-app-banner {
  background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
  border: 1px solid #e2e8f0;
  border-radius: 16px;
  padding: 14px 16px;
  margin: 8px 0 14px 0;
  box-shadow: 0 2px 14px rgba(15, 23, 42, 0.06);
}
.sl-app-banner-grid {
  display: flex;
  align-items: flex-start;
  gap: 14px;
}
.sl-app-banner-icon {
  flex-shrink: 0;
  width: 56px;
  height: 56px;
  border-radius: 14px;
  overflow: hidden;
  border: 1px solid #e2e8f0;
  background: #f1f5f9;
  display: flex;
  align-items: center;
  justify-content: center;
}
.sl-app-banner-icon img {
  width: 56px;
  height: 56px;
  object-fit: cover;
  display: block;
}
.sl-app-banner-body { flex: 1; min-width: 0; }
.sl-app-banner-title {
  font-size: 1.05rem;
  font-weight: 700;
  color: #0f172a;
  line-height: 1.25;
  margin: 0 0 4px 0;
  letter-spacing: -0.02em;
}
.sl-app-banner-meta {
  font-size: 0.82rem;
  color: #64748b;
  font-weight: 500;
  margin: 0 0 8px 0;
}
.sl-app-banner-rating {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 8px;
}
.sl-app-stars {
  display: inline-flex;
  gap: 2px;
  letter-spacing: 0;
}
.sl-star-on { color: #f59e0b; font-size: 1rem; line-height: 1; }
.sl-star-off { color: #e2e8f0; font-size: 1rem; line-height: 1; }
.sl-app-banner-score {
  font-size: 0.95rem;
  font-weight: 700;
  color: #0f172a;
}
.sl-app-banner-score.muted { color: #94a3b8; font-weight: 600; }
</style>
""",
        unsafe_allow_html=True,
    )


def _stars_html(rating: object) -> tuple[str, str]:
    """5 yıldız satırı + sayısal metin (Türkçe ondalık)."""
    if not isinstance(rating, (int, float)) or rating <= 0:
        return (
            '<span class="sl-app-stars">'
            + "".join('<span class="sl-star-off">&#9733;</span>' for _ in range(5))
            + "</span>",
            '<span class="sl-app-banner-score muted">Puan yok</span>',
        )
    r = max(0.0, min(5.0, float(rating)))
    n_on = int(round(r))
    stars_inner = "".join(
        f'<span class="{"sl-star-on" if i < n_on else "sl-star-off"}">&#9733;</span>' for i in range(5)
    )
    score_txt = f"{r:.1f}".replace(".", ",") + " / 5"
    return (
        f'<span class="sl-app-stars" aria-hidden="true">{stars_inner}</span>',
        f'<span class="sl-app-banner-score">{html.escape(score_txt)}</span>',
    )


def _render_app_banner(
    *,
    title: str,
    platform: str,
    icon_url: str,
    rating: object,
    extra_meta: str | None = None,
) -> None:
    t_esc = html.escape(str(title))
    p_esc = html.escape(str(platform))
    extra = f'<div class="sl-app-banner-meta">{html.escape(extra_meta)}</div>' if extra_meta else ""
    stars_h, score_h = _stars_html(rating)
    icon_block = (
        f'<div class="sl-app-banner-icon"><img src="{html.escape(icon_url, quote=True)}" alt="" referrerpolicy="no-referrer"/></div>'
        if icon_url.startswith("http")
        else '<div class="sl-app-banner-icon" style="font-size:0.65rem;font-weight:700;color:#64748b;text-align:center;line-height:1.1;">APP</div>'
    )
    st.markdown(
        f'<div class="sl-app-banner"><div class="sl-app-banner-grid">{icon_block}'
        f'<div class="sl-app-banner-body"><div class="sl-app-banner-title">{t_esc}</div>'
        f'<div class="sl-app-banner-meta">{p_esc}</div>{extra}'
        f'<div class="sl-app-banner-rating">{stars_h}{score_h}</div></div></div></div>',
        unsafe_allow_html=True,
    )


def _banner_play(app_id: str) -> None:
    try:
        from google_play_scraper import app as play_app

        info = play_app(app_id, lang="tr", country="tr")
        title = str(info.get("title", app_id))
        icon = (info.get("icon") or "").strip()
        score = info.get("score")
        genre = info.get("genre") or ""
        if not genre and info.get("categories"):
            c0 = info["categories"][0]
            if isinstance(c0, dict):
                genre = str(c0.get("name", ""))
        _render_app_banner(
            title=title,
            platform="Google Play",
            icon_url=icon,
            rating=score,
            extra_meta=genre if genre else None,
        )
    except Exception:
        _render_app_banner(
            title=f"Seçili: {app_id}",
            platform="Google Play",
            icon_url="",
            rating=None,
            extra_meta="Bilgi alınamadı",
        )


def _banner_ios(app_id: str) -> None:
    import requests

    title = str(app_id)
    icon = ""
    rating: object = None
    genre = ""
    for cc in ("tr", "us", "gb"):
        try:
            r = requests.get(
                f"https://itunes.apple.com/lookup?id={app_id}&country={cc}",
                timeout=6,
            )
            if r.status_code == 200:
                data = r.json().get("results") or []
                if data:
                    a0 = data[0]
                    title = str(a0.get("trackCensoredName") or a0.get("trackName") or app_id)
                    icon = (a0.get("artworkUrl512") or a0.get("artworkUrl100") or "").strip()
                    ar = a0.get("averageUserRating")
                    rating = float(ar) if isinstance(ar, (int, float)) else None
                    genre = str(a0.get("primaryGenreName") or "").strip()
                    break
        except Exception:
            continue
    extra_parts = [p for p in (genre, f"ID {app_id}") if p]
    extra = " · ".join(extra_parts) if extra_parts else None
    _render_app_banner(
        title=title,
        platform="App Store",
        icon_url=icon,
        rating=rating,
        extra_meta=extra,
    )


RANGE_OPTIONS = [
    "Son 1 hafta",
    "Son 1 ay",
    "Son 3 ay",
    "Son 6 ay",
    "Son 1 yıl",
    "Son 2 yıl",
]
RANGE_DAYS = {
    "Son 1 hafta": 7,
    "Son 1 ay": 30,
    "Son 3 ay": 90,
    "Son 6 ay": 180,
    "Son 1 yıl": 365,
    "Son 2 yıl": 730,
}


def render_store_link_tab() -> None:
    _init_store_state()
    _apply_pending_sl_store_input()
    _inject_store_search_css()

    q = st.text_input(
        "Uygulama ara veya mağaza linki / ID",
        key="sl_store_input",
        placeholder="Örn. döviz, com.whatsapp mağaza linki",
        label_visibility="visible",
    )
    text = (q or "").strip()

    if not text and not st.session_state.sl_selected_id:
        st.session_state.sl_search_results = []
        st.session_state.sl_last_query = ""

    resolved, resolve_msg = resolve_direct_input(text)
    if resolve_msg:
        st.info(resolve_msg)

    is_selected = st.session_state.sl_selected_id is not None
    looks_pkg = text.startswith(("com.", "org.", "net.", "io.")) and "." in text

    if is_selected or looks_pkg or (resolved is not None):
        st.session_state.sl_show_search = False
    elif not text:
        st.session_state.sl_show_search = True

    if looks_like_search_keyword(text):
        st.session_state.sl_search_performed = True

    if st.session_state.sl_search_performed:

        def _sl_plat_changed() -> None:
            st.session_state["sl_last_query"] = ""

        st.markdown('<div class="sl-plat-radio-wrap">', unsafe_allow_html=True)
        st.radio(
            "Platform",
            ["Android", "iOS"],
            horizontal=True,
            key="sl_last_filter",
            label_visibility="collapsed",
            on_change=_sl_plat_changed,
        )
        st.markdown("</div>", unsafe_allow_html=True)

        filt = st.session_state.sl_last_filter
        if looks_like_search_keyword(text) and len(text) >= 2:
            if text != st.session_state.sl_last_query or filt != st.session_state.get("_sl_prev_filter"):
                combined: list = []
                if filt == "iOS":
                    combined.extend(search_app_store_itunes(text))
                else:
                    combined.extend(search_play_store(text))
                st.session_state.sl_search_results = combined
                st.session_state.sl_last_query = text
                st.session_state.sl_display_n = 12
                st.session_state._sl_prev_filter = filt

            results = st.session_state.sl_search_results or []
            if results:
                st.markdown(
                    f'<p class="sl-results-head">Bulunan uygulamalar ({len(results)})</p>',
                    unsafe_allow_html=True,
                )
                n_show = min(st.session_state.sl_display_n, len(results))
                for idx, app in enumerate(results[:n_show]):
                    ic, inf, bt = st.columns([0.14, 0.62, 0.24])
                    with ic:
                        icon = app.get("icon") or ""
                        if isinstance(icon, str) and icon.startswith("http"):
                            st.markdown(
                                f'<div class="sl-row-icon"><img src="{icon}" alt=""/></div>',
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
                        if st.button("Seç", key=f"sl_sel_{idx}_{aid}", use_container_width=True):
                            st.session_state.sl_selected_id = aid
                            st.session_state.sl_selected_platform = plat
                            st.session_state.sl_show_search = False
                            st.session_state.sl_search_results = []
                            st.session_state.sl_last_query = ""
                            st.session_state["_pending_sl_store_input"] = aid
                            st.rerun()
                if len(results) > n_show:
                    if st.button("Daha fazla göster", key="sl_more"):
                        st.session_state.sl_display_n = min(st.session_state.sl_display_n + 12, len(results))
                        st.rerun()
            elif len(text) >= 2:
                st.warning("Sonuç bulunamadı. Farklı anahtar kelime veya platform deneyin.")

    r1, r2, r3 = st.columns(3)
    with r1:
        if st.button("Seçimi sıfırla", key="sl_reset"):
            st.session_state.sl_selected_id = None
            st.session_state.sl_selected_platform = None
            st.session_state.sl_show_search = True
            st.session_state.sl_search_results = []
            st.session_state.sl_last_query = ""
            st.session_state.sl_search_performed = False
            st.session_state["_pending_sl_store_input"] = ""
            st.rerun()

    sid = st.session_state.sl_selected_id
    splat = st.session_state.sl_selected_platform

    if sid:
        st.divider()
        if splat == "iOS":
            _banner_ios(str(sid))
        else:
            _banner_play(str(sid))
    elif resolved:
        st.divider()
        if resolved.platform == "ios":
            _banner_ios(resolved.app_id)
        else:
            _banner_play(resolved.app_id)

    time_label = st.selectbox("Tarih aralığı", RANGE_OPTIONS, index=1, key="sl_time_range")
    days = RANGE_DAYS[time_label]

    if st.button("Yorumları çek", type="secondary", use_container_width=True, key="sl_fetch_btn"):
        app_id: str | None = None
        platform: str | None = None

        if st.session_state.sl_selected_id:
            app_id = str(st.session_state.sl_selected_id)
            platform = "ios" if st.session_state.sl_selected_platform == "iOS" else "android"
        elif resolved:
            app_id = resolved.app_id
            platform = resolved.platform
        else:
            st.error("Önce listeden bir uygulama **Seç** deyin veya geçerli paket / ID / ürün linki girin.")
            return

        prog = st.progress(0.0)
        try:
            if platform == "android":
                pool = fetch_google_play_reviews(
                    app_id,
                    days,
                    _progress_callback=lambda x: prog.progress(min(float(x), 1.0)),
                )
            else:
                pool = get_app_store_reviews(
                    app_id,
                    _progress_callback=lambda x: prog.progress(min(float(x), 1.0)),
                    _days_limit=days,
                )
            st.session_state.review_pool_store = pool
            st.session_state.analysis_rows = []
            prog.empty()
            st.caption(f"{len(pool)} benzersiz yorum yüklendi ({time_label}).")
        except Exception as e:
            prog.empty()
            st.error(f"Çekim hatası: {e}")
