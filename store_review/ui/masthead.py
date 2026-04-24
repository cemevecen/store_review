"""Ortak üst bant (masthead): hero başlığı, veri kaynağı pill'leri, dil (bayrak) ve hakkında."""

from __future__ import annotations

import streamlit as st

from store_review.branding import header_logo_data_uri
from store_review.config.i18n import LANGUAGES, get_lang, lang_query_suffix, set_lang, t

SOURCE_OPTIONS = [
    "Mağaza",
    "Dosya",
    "Metin",
    "Uygulama karşılaştır",
]
SOURCE_POOL_KEY = {
    "Mağaza": "store",
    "Dosya": "file",
    "Metin": "paste",
    "Uygulama karşılaştır": "compare",
}
_LEGACY_SOURCE_TAB = {
    "Mağaza (ara / link)": "Mağaza",
    "Dosya yükle": "Dosya",
    "Metin yapıştır": "Metin",
    "Karşılaştır": "Uygulama karşılaştır",
}


def session_main_data_source() -> str:
    """Pills değerini normalize et — eski etiketlerle geriye dönük uyum."""
    v = st.session_state.get("main_data_source_tab")
    if isinstance(v, (list, tuple)):
        v = v[0] if v else None
    if isinstance(v, str):
        v = _LEGACY_SOURCE_TAB.get(v, v)
    if isinstance(v, str) and v in SOURCE_OPTIONS:
        return v
    return SOURCE_OPTIONS[0]


def _on_data_source_change() -> None:
    """Kaynak değişince önceki analiz satırları geçersiz olur."""
    st.session_state.analysis_rows = []


def _on_about_source_change() -> None:
    """About sayfasında pill seçildiğinde ana sayfaya dön + seçimi uygula."""
    st.session_state.analysis_rows = []
    try:
        st.switch_page("streamlit_app.py")
    except Exception:
        pass


def _on_masthead_lang_change() -> None:
    """Selectbox seçenekleri yalnızca bayrak emojisi."""
    label = st.session_state.get("_masthead_lang")
    if not isinstance(label, str):
        return
    for code, _name, flag in LANGUAGES:
        if label == flag:
            set_lang(code)
            return


def render_masthead(*, on_about: bool) -> None:
    """Ana sayfa ve /about sayfasında paylaşılan üst bant.

    Pill'ler her iki sayfada da görünür; about sayfasında seçim yapılırsa
    ana sayfaya dönülür. Dil seçimi yalnızca bayrak gösterir.
    """
    _hdr_uri = header_logo_data_uri()
    logo_html = ""
    if _hdr_uri:
        logo_html = (
            f'<img class="hero-brand-logo" src="{_hdr_uri}" width="48" height="48" alt="" '
            'loading="lazy" decoding="async" />'
        )

    with st.container(border=True, key="pg_masthead", width="stretch"):
        _spacer_l, col_center, _spacer_r = st.columns([1, 10, 1], vertical_alignment="center")
        with col_center:
            st.markdown(
                '<span class="hero-band-target" aria-hidden="true"></span>'
                '<div class="hero-masthead-brand">'
                f"{logo_html}"
                '<h1 class="hero-title">ai store review analysis</h1>'
                "</div>",
                unsafe_allow_html=True,
            )

            _pill_raw = st.session_state.get("main_data_source_tab")
            if isinstance(_pill_raw, (list, tuple)):
                _pill_raw = _pill_raw[0] if _pill_raw else None
            if isinstance(_pill_raw, str):
                _pill_fix = _LEGACY_SOURCE_TAB.get(_pill_raw, _pill_raw)
                if _pill_fix in SOURCE_OPTIONS and _pill_fix != _pill_raw:
                    st.session_state.main_data_source_tab = _pill_fix

            _source_labels = {
                "Mağaza": t("source.store"),
                "Dosya": t("source.file"),
                "Metin": t("source.text"),
                "Uygulama karşılaştır": t("source.compare"),
            }
            st.pills(
                t("nav.data_source"),
                SOURCE_OPTIONS,
                selection_mode="single",
                default=SOURCE_OPTIONS[0],
                format_func=lambda v: _source_labels.get(v, v),
                key="main_data_source_tab",
                label_visibility="collapsed",
                width="stretch",
                on_change=_on_about_source_change if on_about else _on_data_source_change,
            )

            _q = lang_query_suffix()
            _, _ctrl, _ = st.columns([2, 3, 2], vertical_alignment="center")
            with _ctrl:
                c_lang, c_link = st.columns(2, vertical_alignment="center", gap="small")
                with c_lang:
                    cur = get_lang()
                    flag_options = [flag for _c, _n, flag in LANGUAGES]
                    cur_idx = next((i for i, (c, _, _) in enumerate(LANGUAGES) if c == cur), 0)
                    st.selectbox(
                        "lang",
                        options=flag_options,
                        index=cur_idx,
                        key="_masthead_lang",
                        label_visibility="collapsed",
                        on_change=_on_masthead_lang_change,
                    )
                with c_link:
                    if on_about:
                        chip_html = (
                            '<div class="hero-about-chip-wrap">'
                            f'<a class="hero-about-chip" href="./{_q}" '
                            f'aria-label="{t("nav.home")}" title="{t("nav.home")}">'
                            f'<span class="hero-about-chip-dot">x</span>{t("nav.home")}'
                            "</a></div>"
                        )
                    else:
                        chip_html = (
                            '<div class="hero-about-chip-wrap">'
                            f'<a class="hero-about-chip" href="about{_q}" '
                            f'aria-label="{t("nav.about")}" title="{t("nav.about")}">'
                            f'<span class="hero-about-chip-dot">i</span>{t("nav.about")}'
                            "</a></div>"
                        )
                    st.markdown(chip_html, unsafe_allow_html=True)
