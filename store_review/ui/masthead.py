"""Ortak üst bant (masthead): hero başlığı, veri kaynağı pill'leri + hakkında chip'i, sağ üst bayrak dili."""

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


def render_masthead(*, on_about: bool) -> None:
    """Ana sayfa ve /about sayfasında paylaşılan üst bant.

    Dil: sağ üstte yuvarlak bayrak; tıklanınca popover içinde yuvarlak bayrak
    ızgarası. Kaynak pill'lerinin yanında ayrı bir “chip” ile Hakkında / Ana sayfa.
    """
    _hdr_uri = header_logo_data_uri()
    logo_html = ""
    if _hdr_uri:
        logo_html = (
            f'<img class="hero-brand-logo" src="{_hdr_uri}" width="48" height="48" alt="" '
            'loading="lazy" decoding="async" />'
        )

    with st.container(border=True, key="pg_masthead", width="stretch"):
        row_brand, row_lang = st.columns([1, 0.22], vertical_alignment="top")
        with row_brand:
            st.markdown(
                '<span class="hero-band-target" aria-hidden="true"></span>'
                '<div class="hero-masthead-brand hero-masthead-brand--row">'
                f"{logo_html}"
                '<h1 class="hero-title">ai store review analysis</h1>'
                "</div>",
                unsafe_allow_html=True,
            )
        with row_lang:
            with st.container(key="masthead_lang_slot"):
                cur = get_lang()
                cur_flag = next(f for c, _, f in LANGUAGES if c == cur)
                cur_name = next(n for c, n, _ in LANGUAGES if c == cur)
                with st.popover(
                    cur_flag,
                    key="masthead_lang_pop",
                    width=104,
                    help=cur_name,
                    type="secondary",
                ):
                    _per_row = 5
                    for i in range(0, len(LANGUAGES), _per_row):
                        chunk = LANGUAGES[i : i + _per_row]
                        cols = st.columns(len(chunk))
                        for col, (code, name, flag) in zip(cols, chunk):
                            with col:
                                if st.button(flag, key=f"masthead_pick_{code}", help=name):
                                    set_lang(code)
                                    st.rerun()

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
        row_pills, row_about = st.columns([1, 0.26], vertical_alignment="center", gap="small")
        with row_pills:
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
        with row_about:
            _q = lang_query_suffix()
            if on_about:
                chip = (
                    '<div class="masthead-source-pill-wrap">'
                    f'<a class="masthead-source-pill" href="./{_q}" '
                    f'aria-label="{t("nav.home")}" title="{t("nav.home")}">'
                    f'<span class="masthead-source-pill-dot">x</span>{t("nav.home")}'
                    "</a></div>"
                )
            else:
                chip = (
                    '<div class="masthead-source-pill-wrap">'
                    f'<a class="masthead-source-pill" href="about{_q}" '
                    f'aria-label="{t("nav.about")}" title="{t("nav.about")}">'
                    f'<span class="masthead-source-pill-dot">i</span>{t("nav.about")}'
                    "</a></div>"
                )
            st.markdown(chip, unsafe_allow_html=True)
