"""Alt bant (footer) — masthead ile aynı tasarım dili.

Bordered container + marka satırı + etiketli bölümler (dil seçenekleri, hızlı
erişim) ve en altta geliştirici imzası. "Hakkında / ana sayfa" chip'i header'dan
buraya taşındı.
"""

from __future__ import annotations

from urllib.parse import urlparse

import streamlit as st
import streamlit.components.v1 as components

from store_review.branding import header_logo_data_uri
from store_review.config.i18n import LANGUAGES, get_lang, lang_query_suffix, set_lang, t

_FOOTER_CSS = """
<style>
/* =========================================================
   FOOTER LAYOUT
   - Footer varsayılan: viewport altına fixed + translate ile GİZLİ (akışta değil).
   - Yalnızca stMain scroll en dibe gelince body.sr-footer-long--visible ile gösterilir.
   - Kaydırılabilir içerikte stMain’e padding-bottom (JS) — son satırlar footer altında kalmaz.
   .sr-footer-layout-grow: components.html patch ile işaret.
   ========================================================= */

html,
body {
    margin: 0 !important;
    padding: 0 !important;
    min-height: 100% !important;
}

/* stAppViewContainer varsayılanı satır (sidebar | main) — column verme */
.stApp {
    min-height: 100vh !important;
    min-height: 100dvh !important;
}
[data-testid="stAppViewContainer"] {
    min-height: 100vh !important;
    min-height: 100dvh !important;
}

/* Streamlit ana içerik alanı kalan yüksekliği doldursun */
[data-testid="stMain"],
section.main {
    flex: 1 0 auto !important;
    display: flex !important;
    flex-direction: column !important;
    min-height: 0 !important;
    /* Yüzde min-height zinciri için içerik kutusu yüksekliği */
    position: relative !important;
}

/*
 * Kısa sayfa: blok en az kaydırma portunun yüksekliği — footer belgenin dibinde,
 * viewport’a fixed olmadan görünür alanın altına hizalanır.
 */
[data-testid="stMainBlockContainer"] {
    flex: 1 0 auto !important;
    display: flex !important;
    flex-direction: column !important;
    padding-bottom: 0 !important;
    min-height: 100% !important;
    box-sizing: border-box !important;
    align-self: stretch !important;
}

/*
 * stMainBlockContainer çoğu sürümde .block-container sınıfıyla AYNI düğüm.
 * İçerik + footer, doğrudan çocuk stVerticalBlock altında (element-container / layout-wrapper).
 * Footer son stLayoutWrapper içinde — kısa sayfada alta yapışması için o sarmalayıcı büyür.
 */
[data-testid="stMainBlockContainer"] > [data-testid="stVerticalBlock"] {
    flex: 1 0 auto !important;
    display: flex !important;
    flex-direction: column !important;
    align-items: stretch !important;
    min-height: 100% !important;
}

/* Footer’ı saran stLayoutWrapper — belge sonuna itiş (:has + JS sınıfı) */
[data-testid="stMainBlockContainer"] > [data-testid="stVerticalBlock"] > [data-testid="stLayoutWrapper"].sr-footer-layout-grow,
[data-testid="stMainBlockContainer"] > [data-testid="stVerticalBlock"] > [data-testid="stLayoutWrapper"]:last-child:has(.st-key-pg_footer) {
    flex: 1 0 auto !important;
    display: flex !important;
    flex-direction: column !important;
    justify-content: flex-end !important;
    min-height: 0 !important;
}

/* Eski DOM: .block-container ayrı bir çocuk düğüm ise */
[data-testid="stMainBlockContainer"] > .block-container {
    flex: 1 0 auto !important;
    display: flex !important;
    flex-direction: column !important;
    min-height: 0 !important;
}

[data-testid="stMainBlockContainer"] > .block-container > div {
    flex: 1 0 auto !important;
    display: flex !important;
    flex-direction: column !important;
    align-items: stretch !important;
    min-height: 100% !important;
}

/* =========================================================
   FOOTER GÖRSEL TASARIMI
   Mevcut tasarım korunur
   ========================================================= */

.st-key-pg_footer {
    width: 100% !important;
}

.st-key-pg_footer > div {
    width: 100% !important;
}

.custom-footer,
.st-key-pg_footer {
    padding: 26px 42px !important;
    border-radius: 24px 24px 0 0 !important;
    border-top: 1px solid rgba(255, 255, 255, 0.16) !important;
    box-shadow: 0 -14px 36px rgba(15, 23, 42, 0.18) !important;
    background:
        linear-gradient(120deg, #2a070b 0%, #7f1830 45%, #130507 100%) !important;
    color: #0f172a !important;
    overflow: hidden !important;
}

/* Desen katmanı */
.custom-footer::after,
.st-key-pg_footer::after {
    content: "";
    position: absolute;
    inset: 0;
    pointer-events: none;
    opacity: 0.23;
    background-image:
        linear-gradient(rgba(255,255,255,0.23) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255,255,255,0.23) 1px, transparent 1px);
    background-size: 28px 28px;
}

/* Footer içeriği desenin üstünde kalsın */
.custom-footer > *,
.st-key-pg_footer > * {
    position: relative;
    z-index: 1;
}

/* Marka alanı */
.foot-brand {
    display: flex;
    align-items: center;
    gap: 14px;
}

.foot-brand-logo {
    width: 42px;
    height: 42px;
    border-radius: 10px;
    background: #ffffff;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 8px 18px rgba(15, 23, 42, 0.18);
}

.foot-brand-text {
    display: flex;
    flex-direction: column;
    gap: 2px;
}

.foot-brand-title {
    font-weight: 800;
    font-size: 16px;
    line-height: 1.2;
    color: #0f172a;
}

.foot-brand-subtitle {
    font-size: 12px;
    color: #0f172a;
    opacity: 0.85;
}

/* Dil alanı */
.foot-section-label {
    font-size: 13px;
    font-weight: 800;
    letter-spacing: 0.12em;
    text-transform: lowercase;
    color: #0f172a;
    margin-bottom: 10px;
}

.foot-label-spacer {
    height: 24px;
}

/* Selectbox label gizleme */
.st-key-_lang_picker_label label {
    display: none !important;
}

/* Selectbox görünümü */
.st-key-_lang_picker_label [data-baseweb="select"] > div {
    border-radius: 12px !important;
    background: #ffffff !important;
    border: 0 !important;
    box-shadow: none !important;
    min-height: 42px !important;
}

/* Sağ alan */
.foot-col-right {
    display: flex;
    justify-content: flex-end;
    align-items: center;
}

.foot-about-chip,
.foot-home-chip {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    min-height: 40px;
    padding: 0 18px;
    border-radius: 999px;
    background: #ffffff;
    color: #0f172a;
    font-weight: 700;
    text-decoration: none !important;
    box-shadow: 0 8px 18px rgba(15, 23, 42, 0.16);
}

.foot-about-chip:hover,
.foot-home-chip:hover {
    transform: translateY(-1px);
}

/* Mobil */
@media (max-width: 820px) {
    .custom-footer,
    .st-key-pg_footer {
        padding: 20px 18px !important;
        border-radius: 20px 20px 0 0 !important;
    }

    .foot-brand {
        justify-content: center;
        text-align: center;
        margin-bottom: 16px;
    }

    .foot-section-label {
        text-align: center;
    }

    .foot-col-right {
        justify-content: center;
        margin-top: 16px;
    }

    .st-key-_lang_picker_label {
        width: 100% !important;
    }
}

/*
 * JS patch gelene kadar (footer DOM’da yok / erken boyama): akışta relative.
 * body.sr-footer-long ile aşağıdaki fixed + gizli/görünür kuralları baskın gelir.
 */
body:not(.sr-footer-long) footer.custom-footer,
body:not(.sr-footer-long) div[data-testid="custom-footer"],
body:not(.sr-footer-long) .custom-footer,
body:not(.sr-footer-long) .st-key-pg_footer,
body:not(.sr-footer-long) [data-testid="stVerticalBlock"].st-key-pg_footer,
body:not(.sr-footer-long) [data-testid="stVerticalBlockBorderWrapper"].st-key-pg_footer,
body:not(.sr-footer-long) [class*="st-key-pg_footer"] {
    position: relative !important;
    top: auto !important;
    right: auto !important;
    bottom: auto !important;
    left: auto !important;
    inset: auto !important;
    z-index: auto !important;
    transform: none !important;

    width: 100% !important;
    max-width: 100% !important;
    flex-shrink: 0 !important;
    box-sizing: border-box !important;

    margin-top: 0 !important;
    margin-bottom: 0 !important;
}

/* Footer yüzünden içerik alttan boşluk bırakmasın */
body .stApp,
body [data-testid="stAppViewContainer"],
body [data-testid="stMainBlockContainer"] {
    padding-bottom: 0 !important;
}

body .stApp,
body [data-testid="stAppViewContainer"] {
    min-height: 100vh !important;
    min-height: 100dvh !important;
}

/* ----- Dock: footer sadece stMain scroll en dibe gelince ----- */
body.sr-footer-long [data-testid="stMainBlockContainer"] > [data-testid="stVerticalBlock"] > [data-testid="stLayoutWrapper"].sr-footer-layout-grow,
body.sr-footer-long [data-testid="stMainBlockContainer"] > [data-testid="stVerticalBlock"] > [data-testid="stLayoutWrapper"]:last-child:has(.st-key-pg_footer) {
    flex: 0 0 auto !important;
    justify-content: flex-start !important;
}

body.sr-footer-long .st-key-pg_footer,
body.sr-footer-long [data-testid="stVerticalBlock"].st-key-pg_footer,
body.sr-footer-long [data-testid="stVerticalBlockBorderWrapper"].st-key-pg_footer {
    position: fixed !important;
    left: 0 !important;
    right: 0 !important;
    bottom: 0 !important;
    top: auto !important;
    width: 100% !important;
    max-width: 100% !important;
    margin: 0 !important;
    z-index: 25 !important;
    transform: translateY(110%) !important;
    transition: transform 0.22s ease-out !important;
    pointer-events: none !important;
}

body.sr-footer-long.sr-footer-long--visible .st-key-pg_footer,
body.sr-footer-long.sr-footer-long--visible [data-testid="stVerticalBlock"].st-key-pg_footer,
body.sr-footer-long.sr-footer-long--visible [data-testid="stVerticalBlockBorderWrapper"].st-key-pg_footer {
    transform: translateY(0) !important;
    pointer-events: auto !important;
}
</style>
"""

# st.markdown <script> çalışmaz; file_uploader yaması gibi parent belgede components.html ile işler.
_FOOTER_DOM_PATCH_HTML = """
<script>
(function () {
  var root;
  try {
    root = window.top;
  } catch (e) {
    root = window.parent;
  }
  if (!root || root.__srFooterLayoutPatch) return;

  function resolveAppDoc() {
    var list = [];
    try {
      if (window.top) list.push(window.top.document);
    } catch (e) {}
    try {
      if (window.parent && window.parent !== window) list.push(window.parent.document);
    } catch (e2) {}
    if (root && root.document) list.push(root.document);
    for (var i = 0; i < list.length; i++) {
      var d = list[i];
      if (d && d.querySelector('[data-testid="stMain"]')) return d;
    }
    return root.document;
  }

  var TH = 24;
  var mbcRo = null;
  function ensureScrollOnMain() {
    var doc = resolveAppDoc();
    var main = doc.querySelector('[data-testid="stMain"]');
    if (!main) return;
    if (!root.__srFooterScrollOnMain) {
      root.__srFooterScrollOnMain = true;
      main.addEventListener("scroll", scheduleLongFooter, { passive: true });
    }
    if (!root.__srFooterMainRo && typeof ResizeObserver !== "undefined") {
      root.__srFooterMainRo = new ResizeObserver(scheduleLongFooter);
      root.__srFooterMainRo.observe(main);
    }
  }
  function ensureMbcResize() {
    if (mbcRo) return;
    var doc = resolveAppDoc();
    var mbc = doc.querySelector('[data-testid="stMainBlockContainer"]');
    if (!mbc || typeof ResizeObserver === "undefined") return;
    mbcRo = new ResizeObserver(scheduleLongFooter);
    mbcRo.observe(mbc);
  }
  function mark() {
    var doc = resolveAppDoc();
    doc.querySelectorAll(".sr-footer-layout-grow").forEach(function (w) {
      w.classList.remove("sr-footer-layout-grow");
    });
    doc.querySelectorAll(
      '[data-testid="stVerticalBlock"].st-key-pg_footer, [data-testid="stVerticalBlockBorderWrapper"].st-key-pg_footer'
    ).forEach(function (el) {
      el.classList.add("custom-footer");
      var p = el.parentElement;
      if (p && p.getAttribute("data-testid") === "stLayoutWrapper") {
        p.classList.add("sr-footer-layout-grow");
      }
    });
    initLongFooterOnce();
    ensureScrollOnMain();
    ensureMbcResize();
    scheduleLongFooter();
  }
  function syncLongFooter() {
    var doc = resolveAppDoc();
    var main = doc.querySelector('[data-testid="stMain"]');
    var mbc = doc.querySelector('[data-testid="stMainBlockContainer"]');
    var foot = doc.querySelector(
      '[data-testid="stVerticalBlock"].st-key-pg_footer, [data-testid="stVerticalBlockBorderWrapper"].st-key-pg_footer'
    );
    var body = doc.body;
    if (!main || !body) return;

    if (!foot) {
      body.classList.remove("sr-footer-long", "sr-footer-long--visible");
      main.style.paddingBottom = "";
      return;
    }

    var ch = main.clientHeight;
    body.classList.add("sr-footer-long");
    var h = Math.max(foot.offsetHeight || 0, 80);
    /* Ölçüm: padding olmadan içerik yüksekliği — kısa sayfada ekstra boşluk zorlamayız */
    main.style.paddingBottom = "";
    var shContent = Math.max(main.scrollHeight, mbc ? mbc.scrollHeight : 0);
    var scrollable = shContent > ch + TH;
    if (scrollable) {
      main.style.paddingBottom = Math.ceil(h) + "px";
    }

    var sh = Math.max(main.scrollHeight, mbc ? mbc.scrollHeight : 0);
    var st = main.scrollTop;
    var atBottom = st + ch >= sh - TH;
    if (atBottom) body.classList.add("sr-footer-long--visible");
    else body.classList.remove("sr-footer-long--visible");
  }
  function scheduleLongFooter() {
    root.setTimeout(syncLongFooter, 0);
  }
  function initLongFooterOnce() {
    if (root.__srFooterLongScrollInit) return;
    root.__srFooterLongScrollInit = true;
    root.addEventListener("resize", scheduleLongFooter);
    resolveAppDoc().addEventListener("visibilitychange", scheduleLongFooter);
    /* Streamlit bazı güncellemelerde MutationObserver tetiklenmeyebilir */
    if (!root.__srFooterPoll) {
      root.__srFooterPoll = root.setInterval(syncLongFooter, 1200);
    }
  }
  function boot() {
    if (root.__srFooterLayoutPatch) return;
    var doc = resolveAppDoc();
    if (!doc.body) return;
    mark();
    if (!root.__srFooterClassObserver) {
      root.__srFooterClassObserver = new MutationObserver(mark);
      root.__srFooterClassObserver.observe(doc.body, { childList: true, subtree: true });
    }
    root.__srFooterLayoutPatch = true;
  }
  boot();
  [50, 200, 600, 1500].forEach(function (ms) { setTimeout(boot, ms); });
})();
</script>
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
    if not st.session_state.get("_sr_footer_dom_patch"):
        st.session_state["_sr_footer_dom_patch"] = True
        components.html(_FOOTER_DOM_PATCH_HTML, height=0, width=0)

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
