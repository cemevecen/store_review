"""Alt bant (footer) — dil seçenekleri bloğu.

Bayrak + dil isimli bir dropdown sunar; seçim değişince tüm çevrilmiş stringler
otomatik olarak yeni dile göre render edilir.
"""

from __future__ import annotations

import streamlit as st

from store_review.config.i18n import LANGUAGES, get_lang, set_lang, t

_FOOTER_CSS = """
<style>
.app-footer {
  margin: 28px auto 12px;
  padding: 16px 18px 14px;
  max-width: 820px;
  border: 1px solid #e2e8f0;
  border-radius: 18px;
  background: linear-gradient(180deg,#ffffff 0%, #f8fafc 100%);
  box-shadow: 0 1px 6px rgba(15, 23, 42, 0.04);
}
.app-footer-title {
  font-size: 0.78rem;
  color: #64748b;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  margin: 0 0 8px 0;
}
.app-footer-meta {
  font-size: 0.78rem;
  color: #94a3b8;
  text-align: center;
  margin: 10px 0 0 0;
}
[data-testid="stVerticalBlock"].st-key-app_footer_lang_row [data-testid="stSelectbox"] {
  margin-top: 0 !important;
}
@media (max-width: 640px) {
  .app-footer { margin: 20px 10px; padding: 14px; border-radius: 14px; }
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


def render_footer() -> None:
    st.markdown(_FOOTER_CSS, unsafe_allow_html=True)
    st.markdown('<div class="app-footer">', unsafe_allow_html=True)
    st.markdown(
        f'<p class="app-footer-title">{t("footer.language_options")}</p>',
        unsafe_allow_html=True,
    )

    cur = get_lang()
    options = [f"{flag}  {name}" for code, name, flag in LANGUAGES]
    cur_idx = next((i for i, (c, _, _) in enumerate(LANGUAGES) if c == cur), 0)

    with st.container(key="app_footer_lang_row"):
        st.selectbox(
            t("footer.language_options"),
            options=options,
            index=cur_idx,
            key="_lang_picker_label",
            label_visibility="collapsed",
            on_change=_on_lang_change,
        )

    st.markdown(
        f'<p class="app-footer-meta">{t("footer.developed_by")}</p>',
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)
