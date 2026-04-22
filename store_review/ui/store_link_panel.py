"""
Tek mağaza sekmesi: isim araması (Play + App Store), Android/iOS filtresi, sonuçtan seçim, tarih aralığı, çekme.
Eski monolitik streamlit_app "Mağaza Linki" akışının sadeleştirilmiş hali.
"""

from __future__ import annotations

import html

import streamlit as st

from store_review.fetchers.app_discovery import (
    ResolvedApp,
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
.sl-results-head {
  font-size:0.82rem; color:#64748b; font-weight:700; text-transform:uppercase;
  letter-spacing:0.06em; margin:6px 0 10px;
}
.sl-row-icon img { width:40px; height:40px; border-radius:50%; object-fit:cover; display:block; }
.sl-row-title { font-weight:700; color:#0f172a; font-size:0.9rem; line-height:1.25; }
.sl-row-id { font-size:0.72rem; color:#94a3b8; margin-top:2px; word-break:break-all; }
input::placeholder { opacity: 1 !important; color: #64748b !important; }
</style>
""",
        unsafe_allow_html=True,
    )


def _banner_play(app_id: str) -> None:
    try:
        from google_play_scraper import app as play_app

        info = play_app(app_id, lang="tr", country="tr")
        title = info.get("title", app_id)
        icon = (info.get("icon") or "").strip()
        score = info.get("score")
        sc = f"{score:.1f} ★" if isinstance(score, (int, float)) else "—"
        col_a, col_b = st.columns([0.15, 0.85])
        with col_a:
            if icon.startswith("http"):
                st.image(icon, width=56)
        with col_b:
            st.success(f"**{title}** · Google Play · Mağaza puanı: {sc}")
    except Exception:
        st.success(f"Seçili uygulama: `{app_id}` (Google Play)")


def _banner_ios(app_id: str) -> None:
    import requests

    title = app_id
    icon = ""
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
                    title = a0.get("trackCensoredName") or a0.get("trackName") or app_id
                    icon = (a0.get("artworkUrl512") or a0.get("artworkUrl100") or "").strip()
                    break
        except Exception:
            continue
    col_a, col_b = st.columns([0.15, 0.85])
    with col_a:
        if icon.startswith("http"):
            st.image(icon, width=56)
    with col_b:
        st.success(f"**{title}** · App Store · ID `{app_id}`")


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
    _inject_store_search_css()

    st.caption(
        "Uygulama **adı** yazarak arayın (aşağıda listelenir) veya **paket** (`com…`), **App Store ID**, "
        "**Play / App Store ürün linki** girin."
    )

    q = st.text_input(
        "Uygulama ara veya mağaza linki / ID",
        key="sl_store_input",
        placeholder="Örn: döviz  ·  com.whatsapp  ·  mağaza linki",
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
        pc1, pc2 = st.columns(2)
        with pc1:
            if st.button("Android", use_container_width=True, key="sl_pf_android"):
                st.session_state.sl_last_filter = "Android"
                st.session_state.sl_last_query = ""
                st.rerun()
        with pc2:
            if st.button("iOS", use_container_width=True, key="sl_pf_ios"):
                st.session_state.sl_last_filter = "iOS"
                st.session_state.sl_last_query = ""
                st.rerun()

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
                            st.markdown('<div style="font-size:1.6rem;">📱</div>', unsafe_allow_html=True)
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
                            st.session_state["sl_store_input"] = aid
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
            st.session_state["sl_store_input"] = ""
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

    st.caption("Apple: mağaza linki veya sayısal ID. Play: link veya `com…` paket adı. İsim araması için yukarıda Android/iOS seçin.")

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
            st.session_state.review_pool = pool
            st.session_state.analysis_rows = []
            prog.empty()
            st.success(f"{len(pool)} benzersiz yorum yüklendi ({time_label}).")
        except Exception as e:
            prog.empty()
            st.error(f"Çekim hatası: {e}")
