"""Alt bant (footer) — masthead ile aynı tasarım dili.

Bordered container + marka satırı + etiketli bölümler (dil seçenekleri, hızlı
erişim) ve en altta geliştirici imzası. "Hakkında / ana sayfa" chip'i header'dan
buraya taşındı.
"""

from __future__ import annotations

from urllib.parse import urlparse

import streamlit as st

from store_review.branding import header_logo_data_uri
from store_review.config.i18n import LANGUAGES, get_lang, lang_query_suffix, set_lang, t

_FOOTER_CSS = """
<style>
/*
 * Alta itilen footer (document flow) — position fixed/sticky yok. Kısa sayfada viewport dibine,
 * uzun sayfada içeriğin sonuna; scroll ile ekranda kalmaz.
 * stAppViewContainer satır flex — column yapılmaz (sidebar).
 */
html, body {
  margin: 0 !important;
  padding: 0 !important;
  min-height: 100dvh !important;
}
.stApp {
  min-height: 100vh !important;
  min-height: 100dvh !important;
  display: flex !important;
  flex-direction: column !important;
  box-sizing: border-box !important;
}
[data-testid="stAppViewContainer"] {
  min-height: 100dvh !important;
  flex: 1 1 auto !important;
}
[data-testid="stAppScrollToBottomContainer"],
[data-testid="stAppViewContainer"] section.stMain,
[data-testid="stAppViewContainer"] section.main {
  flex: 1 1 auto !important;
  display: flex !important;
  flex-direction: column !important;
  align-items: stretch !important;
  min-height: 100dvh !important;
  min-width: 0 !important;
}
[data-testid="stMainBlockContainer"] {
  flex: 1 1 auto !important;
  display: flex !important;
  flex-direction: column !important;
  min-height: 0 !important;
  width: 100% !important;
  padding-bottom: 0 !important;
  margin-bottom: 0 !important;
}
[data-testid="stMainBlockContainer"] > [data-testid="stVerticalBlock"],
[data-testid="stMainBlockContainer"] > [data-testid="stVerticalBlockBorderWrapper"] {
  flex: 1 1 auto !important;
  display: flex !important;
  flex-direction: column !important;
  min-height: 0 !important;
}
[data-testid="stMainBlockContainer"] > *:first-child {
  flex: 1 1 auto !important;
  display: flex !important;
  flex-direction: column !important;
  min-height: 0 !important;
  align-self: stretch !important;
}

/* Footer — masthead ile aynı bordo gradient; akış içi, alta itilir. */
[data-testid="stVerticalBlock"].st-key-pg_footer,
[data-testid="stVerticalBlockBorderWrapper"].st-key-pg_footer {
  flex-shrink: 0 !important;
  width: 100vw !important;
  min-width: 100vw !important;
  max-width: 100vw !important;
  position: relative !important;
  left: 50% !important;
  transform: translateX(-50%) !important;
  margin-left: 0 !important;
  margin-right: 0 !important;
  margin-top: auto !important;
  margin-bottom: 0 !important;
  padding: 26px clamp(18px, 4vw, 44px) 22px !important;
  box-sizing: border-box !important;
  border: none !important;
  border-radius: 22px 22px 0 0 !important;
  border-top: 1px solid rgba(0, 0, 0, 0.14) !important;
  box-shadow: 0 -10px 32px rgba(48, 8, 16, 0.34) !important;
  overflow: hidden !important;
  background: linear-gradient(
    282deg,
    #120608 0%,
    #1f0a0e 18%,
    #3a0f18 40%,
    #5c1524 62%,
    #7a1f30 82%,
    #8f2840 100%
  ) !important;
}
[data-testid="stAppScrollToBottomContainer"] [data-testid="element-container"]:has(
  > [data-testid="stVerticalBlockBorderWrapper"].st-key-pg_footer
),
[data-testid="stAppScrollToBottomContainer"] [data-testid="element-container"]:has(
  > [data-testid="stVerticalBlock"].st-key-pg_footer
),
[data-testid="stAppViewContainer"] section.stMain [data-testid="element-container"]:has(
  > [data-testid="stVerticalBlockBorderWrapper"].st-key-pg_footer
),
[data-testid="stAppViewContainer"] section.stMain [data-testid="element-container"]:has(
  > [data-testid="stVerticalBlock"].st-key-pg_footer
),
[data-testid="stAppScrollToBottomContainer"] [data-testid="stVerticalBlock"] > [data-testid="stVerticalBlockBorderWrapper"].st-key-pg_footer,
[data-testid="stAppScrollToBottomContainer"] [data-testid="stVerticalBlock"] > [data-testid="stVerticalBlock"].st-key-pg_footer,
[data-testid="stAppViewContainer"] section.stMain [data-testid="stVerticalBlock"] > [data-testid="stVerticalBlockBorderWrapper"].st-key-pg_footer,
[data-testid="stAppViewContainer"] section.stMain [data-testid="stVerticalBlock"] > [data-testid="stVerticalBlock"].st-key-pg_footer {
  margin-top: auto !important;
  margin-bottom: 0 !important;
  width: 100% !important;
}

[data-testid="stVerticalBlock"].st-key-pg_footer::after,
[data-testid="stVerticalBlockBorderWrapper"].st-key-pg_footer::after {
  content: "" !important;
  position: absolute !important;
  inset: 0 !important;
  pointer-events: none !important;
  border-radius: inherit !important;
  opacity: 0.05 !important;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24'%3E%3Cpath fill='%23ffffff' d='M11 5h2v6h6v2h-6v6h-2v-6H5v-2h6z'/%3E%3C/svg%3E") !important;
  background-size: 24px 24px !important;
}
.foot-brand {
  display: flex;
  align-items: center;
  gap: 12px;
  margin: 0;
  position: relative;
  z-index: 1;
  min-height: 48px;
}
.foot-brand-logo {
  width: 40px;
  height: 40px;
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.08);
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.22);
}
.foot-brand-text {
  display: flex;
  flex-direction: column;
  line-height: 1.15;
}
.foot-brand-title {
  font-size: 1rem;
  font-weight: 700;
  color: #ffffff;
  letter-spacing: -0.01em;
}
.foot-brand-sub {
  font-size: 0.76rem;
  color: rgba(255, 255, 255, 0.68);
  margin-top: 3px;
}
.foot-section-label {
  font-size: 0.72rem;
  font-weight: 700;
  color: rgba(255, 255, 255, 0.72);
  letter-spacing: 0.09em;
  text-transform: uppercase;
  margin: 0 0 8px 0;
  position: relative;
  z-index: 1;
}
.foot-label-spacer {
  height: 20px;
  margin: 0 0 8px 0;
  visibility: hidden;
  pointer-events: none;
}

/* Dil dropdown'ı: içeriğe yetecek kadar dar. */
[data-testid="stVerticalBlock"].st-key-pg_footer .st-key-_lang_picker_label,
[data-testid="stVerticalBlockBorderWrapper"].st-key-pg_footer .st-key-_lang_picker_label {
  max-width: 260px !important;
  width: 100% !important;
  position: relative;
  z-index: 1;
}
[data-testid="stVerticalBlock"].st-key-pg_footer [data-testid="stSelectbox"] > label,
[data-testid="stVerticalBlockBorderWrapper"].st-key-pg_footer [data-testid="stSelectbox"] > label {
  display: none !important;
  height: 0 !important;
  margin: 0 !important;
}
/* Dropdown gövdesini koyu zeminde de okunur göster. */
[data-testid="stVerticalBlock"].st-key-pg_footer div[data-baseweb="select"] > div,
[data-testid="stVerticalBlockBorderWrapper"].st-key-pg_footer div[data-baseweb="select"] > div {
  background: rgba(255, 255, 255, 0.96) !important;
  border: 1px solid rgba(255, 255, 255, 0.28) !important;
  border-radius: 12px !important;
  color: #1f2937 !important;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.18) !important;
}
[data-testid="stVerticalBlock"].st-key-pg_footer div[data-baseweb="select"] svg,
[data-testid="stVerticalBlockBorderWrapper"].st-key-pg_footer div[data-baseweb="select"] svg {
  fill: #4b5563 !important;
  color: #4b5563 !important;
}
/* Dil dropdown'ı yazılabilir olmasın: caret/imleç gizli, metin alanı read-only hissi. */
[data-testid="stVerticalBlock"].st-key-pg_footer div[data-baseweb="select"] input,
[data-testid="stVerticalBlockBorderWrapper"].st-key-pg_footer div[data-baseweb="select"] input {
  caret-color: transparent !important;
  cursor: pointer !important;
  user-select: none !important;
}
[data-testid="stVerticalBlock"].st-key-pg_footer div[data-baseweb="select"] input:focus,
[data-testid="stVerticalBlockBorderWrapper"].st-key-pg_footer div[data-baseweb="select"] input:focus {
  outline: none !important;
}

.foot-col-right {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 48px;
  padding-right: 0;
  position: relative;
  z-index: 1;
}
.foot-about-chip-wrap {
  display: inline-flex;
  align-items: center;
  justify-content: center;
}
.foot-about-chip {
  display: inline-flex;
  align-items: center;
  gap: 7px;
  padding: 8px 16px;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.95);
  color: #c2410c;
  font-weight: 600;
  font-size: 0.85rem;
  text-decoration: none;
  border: 1px solid rgba(255, 237, 213, 0.6);
  transition: transform 0.15s ease, box-shadow 0.15s ease, filter 0.15s ease;
}
.foot-about-chip:hover {
  text-decoration: none;
  filter: brightness(1.04);
  box-shadow: 0 4px 16px rgba(234, 88, 12, 0.28);
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
/* Yatay tek satır: marka | dil | chip — dikey ortalı ve geniş boşluklu. */
[data-testid="stVerticalBlock"].st-key-pg_footer [data-testid="stHorizontalBlock"],
[data-testid="stVerticalBlockBorderWrapper"].st-key-pg_footer [data-testid="stHorizontalBlock"] {
  align-items: center !important;
  gap: 24px !important;
}

@media (max-width: 820px) {
  [data-testid="stVerticalBlock"].st-key-pg_footer,
  [data-testid="stVerticalBlockBorderWrapper"].st-key-pg_footer {
    padding: 22px clamp(14px, 4vw, 20px) 18px !important;
  }
  [data-testid="stVerticalBlock"].st-key-pg_footer [data-testid="stHorizontalBlock"],
  [data-testid="stVerticalBlockBorderWrapper"].st-key-pg_footer [data-testid="stHorizontalBlock"] {
    flex-direction: column !important;
    align-items: stretch !important;
    gap: 14px !important;
  }
  [data-testid="stVerticalBlock"].st-key-pg_footer .st-key-_lang_picker_label,
  [data-testid="stVerticalBlockBorderWrapper"].st-key-pg_footer .st-key-_lang_picker_label {
    max-width: 100% !important;
  }
  .foot-col-right {
    justify-content: flex-start;
    margin-top: 0;
    padding-right: 0;
  }
  .foot-about-chip-wrap { justify-content: flex-start; width: 100%; }
  .foot-brand { min-height: 0; }
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
        col_brand, col_lang, col_about = st.columns(
            [1, 1, 1], vertical_alignment="center", gap="medium"
        )

        with col_brand:
            st.markdown(
                f'<div class="foot-brand">{logo_html}'
                '<div class="foot-brand-text">'
                '<span class="foot-brand-title">ai store review analysis</span>'
                f'<span class="foot-brand-sub">{t("footer.developed_by")}</span>'
                "</div></div>",
                unsafe_allow_html=True,
            )

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
            st.markdown('<div class="foot-label-spacer" aria-hidden="true"></div>', unsafe_allow_html=True)
            _q = lang_query_suffix()
            if on_about:
                chip_html = (
                    '<div class="foot-col-right"><div class="foot-about-chip-wrap">'
                    f'<a class="foot-about-chip" href="./{_q}" '
                    f'aria-label="{t("nav.home")}" title="{t("nav.home")}">'
                    f'<span class="foot-about-chip-dot">x</span>{t("nav.home")}'
                    "</a></div></div>"
                )
            else:
                chip_html = (
                    '<div class="foot-col-right"><div class="foot-about-chip-wrap">'
                    f'<a class="foot-about-chip" href="about{_q}" '
                    f'aria-label="{t("nav.about")}" title="{t("nav.about")}">'
                    f'<span class="foot-about-chip-dot">i</span>{t("nav.about")}'
                    "</a></div></div>"
                )
            st.markdown(chip_html, unsafe_allow_html=True)
