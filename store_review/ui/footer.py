"""Alt bant (footer) — masthead ile aynı tasarım dili.

Bordered container + marka satırı + etiketli bölümler (dil seçenekleri, hızlı
erişim) ve en altta geliştirici imzası. "Hakkında / ana sayfa" chip'i header'dan
buraya taşındı.
"""

from __future__ import annotations

from urllib.parse import urlparse

import streamlit as st

from store_review.branding import header_logo_data_uri
from store_review.config.i18n import LANGUAGES, get_lang, set_lang, t

_FOOTER_CSS = """
<style>
[data-testid="stVerticalBlock"].st-key-pg_footer,
[data-testid="stVerticalBlockBorderWrapper"].st-key-pg_footer {
  margin-top: 34px !important;
}
[data-testid="stVerticalBlockBorderWrapper"].st-key-pg_footer {
  background: linear-gradient(180deg,#ffffff 0%, #f8fafc 100%) !important;
  border: 1px solid #e2e8f0 !important;
  border-radius: 22px !important;
  box-shadow: 0 1px 10px rgba(15, 23, 42, 0.04) !important;
  padding: 22px 22px 18px !important;
}
.foot-brand {
  display: flex;
  align-items: center;
  gap: 12px;
  margin: 0 0 14px 0;
}
.foot-brand-logo {
  width: 36px;
  height: 36px;
  border-radius: 10px;
}
.foot-brand-text {
  display: flex;
  flex-direction: column;
  line-height: 1.1;
}
.foot-brand-title {
  font-size: 0.95rem;
  font-weight: 700;
  color: #0f172a;
  letter-spacing: -0.01em;
}
.foot-brand-sub {
  font-size: 0.75rem;
  color: #64748b;
  margin-top: 2px;
}
.foot-section-label {
  font-size: 0.72rem;
  font-weight: 700;
  color: #64748b;
  letter-spacing: 0.09em;
  text-transform: uppercase;
  margin: 0 0 8px 0;
}
.foot-col-right {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  min-height: 100%;
}
.foot-about-chip-wrap {
  display: inline-flex;
  align-items: center;
  justify-content: flex-end;
}
.foot-about-chip {
  display: inline-flex;
  align-items: center;
  gap: 7px;
  padding: 8px 16px;
  border-radius: 999px;
  background: linear-gradient(90deg,#fff7ed,#ffedd5);
  color: #c2410c;
  font-weight: 600;
  font-size: 0.85rem;
  text-decoration: none;
  border: 1px solid #fed7aa;
  transition: transform 0.15s ease, box-shadow 0.15s ease, filter 0.15s ease;
}
.foot-about-chip:hover {
  text-decoration: none;
  filter: brightness(1.02);
  box-shadow: 0 4px 14px rgba(234, 88, 12, 0.16);
  transform: translateY(-1px);
}
.foot-about-chip-dot {
  width: 18px;
  height: 18px;
  border-radius: 50%;
  background: #ea580c;
  color: #fff;
  font-size: 0.68rem;
  font-weight: 700;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  line-height: 1;
}
.foot-divider {
  height: 1px;
  background: linear-gradient(90deg, transparent 0%, #e2e8f0 20%, #e2e8f0 80%, transparent 100%);
  margin: 14px 0 10px 0;
}
.foot-meta {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 8px;
  font-size: 0.76rem;
  color: #94a3b8;
}
.foot-meta-dot {
  width: 4px;
  height: 4px;
  border-radius: 50%;
  background: #cbd5e1;
}
[data-testid="stVerticalBlock"].st-key-pg_footer [data-testid="stSelectbox"] > label {
  display: none !important;
  height: 0 !important;
  margin: 0 !important;
}
@media (max-width: 720px) {
  [data-testid="stVerticalBlockBorderWrapper"].st-key-pg_footer {
    padding: 18px 16px 14px !important;
    border-radius: 18px !important;
  }
  .foot-col-right { justify-content: flex-start; margin-top: 12px; }
  .foot-about-chip-wrap { justify-content: flex-start; width: 100%; }
}
</style>
"""


def _on_lang_change() -> None:
    label = st.session_state.get("_lang_picker_label")
    if not isinstance(label, str):
        return
    for code, name, flag in LANGUAGES:
        if label == f"{flag}  {name}":
            set_lang(code)
            return


def _on_about_page() -> bool:
    """Mevcut sayfa /about ise chip 'ana sayfa' göstermeli."""
    try:
        ctx = st.context
        url_raw = getattr(ctx, "url", None)
        if url_raw:
            path = urlparse(str(url_raw)).path or "/"
            if path.endswith("/about") or path.endswith("/about/"):
                return True
    except Exception:
        pass
    # Fallback: sayfa /about olduğunda app_about_page flag'ini set ederiz.
    return bool(st.session_state.get("_on_about_page"))


def render_footer(*, on_about: bool | None = None) -> None:
    """Footer — header'la aynı kart dili; dil seçenekleri + hakkında chip'i içerir."""
    st.markdown(_FOOTER_CSS, unsafe_allow_html=True)

    # Explicit override yoksa session state / URL üzerinden tahmin et.
    if on_about is None:
        on_about = _on_about_page()

    _hdr_uri = header_logo_data_uri()
    logo_html = ""
    if _hdr_uri:
        logo_html = (
            f'<img class="foot-brand-logo" src="{_hdr_uri}" width="36" height="36" alt="" '
            'loading="lazy" decoding="async" />'
        )

    with st.container(border=True, key="pg_footer", width="stretch"):
        st.markdown(
            f'<div class="foot-brand">{logo_html}'
            '<div class="foot-brand-text">'
            '<span class="foot-brand-title">ai store review analysis</span>'
            f'<span class="foot-brand-sub">{t("footer.developed_by")}</span>'
            "</div></div>",
            unsafe_allow_html=True,
        )

        col_lang, col_about = st.columns([2, 1], vertical_alignment="center")

        with col_lang:
            st.markdown(
                f'<p class="foot-section-label">{t("footer.language_options")}</p>',
                unsafe_allow_html=True,
            )
            cur = get_lang()
            options = [f"{flag}  {name}" for _, name, flag in LANGUAGES]
            cur_idx = next((i for i, (c, _, _) in enumerate(LANGUAGES) if c == cur), 0)
            st.selectbox(
                t("footer.language_options"),
                options=options,
                index=cur_idx,
                key="_lang_picker_label",
                label_visibility="collapsed",
                on_change=_on_lang_change,
            )

        with col_about:
            st.markdown(
                f'<p class="foot-section-label">{t("footer.quick_access")}</p>',
                unsafe_allow_html=True,
            )
            if on_about:
                chip_html = (
                    '<div class="foot-col-right"><div class="foot-about-chip-wrap">'
                    f'<a class="foot-about-chip" href="./" '
                    f'aria-label="{t("nav.home")}" title="{t("nav.home")}">'
                    f'<span class="foot-about-chip-dot">x</span>{t("nav.home")}'
                    "</a></div></div>"
                )
            else:
                chip_html = (
                    '<div class="foot-col-right"><div class="foot-about-chip-wrap">'
                    f'<a class="foot-about-chip" href="about" '
                    f'aria-label="{t("nav.about")}" title="{t("nav.about")}">'
                    f'<span class="foot-about-chip-dot">i</span>{t("nav.about")}'
                    "</a></div></div>"
                )
            st.markdown(chip_html, unsafe_allow_html=True)

        st.markdown('<div class="foot-divider"></div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="foot-meta">'
            f'<span>{t("footer.developed_by")}</span>'
            '<span class="foot-meta-dot"></span>'
            '<span>ai store review analysis</span>'
            "</div>",
            unsafe_allow_html=True,
        )
