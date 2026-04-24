"""/about — Hakkında sayfası (Streamlit multi-page).

URL: /about
Ana sayfadaki header / pill / chip yapısı burada da korunur. Pill'e tıklanırsa
ana sayfaya dönülüp seçilen kaynak aktifleştirilir.
"""

from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from store_review.branding import ensure_branding_assets, favicon_abs_path
from store_review.config.theme import APP_CSS
from store_review.ui.masthead import render_masthead


def _inject_css() -> None:
    st.markdown(f"<style>{APP_CSS}</style>", unsafe_allow_html=True)


def _render_about_body() -> None:
    st.markdown('<p class="section-title">hakkında</p>', unsafe_allow_html=True)
    lang_pick = st.segmented_control(
        "Dil",
        options=["TR", "ENG"],
        selection_mode="single",
        default="TR",
        key="about_lang",
        label_visibility="collapsed",
        width="content",
    )
    lang = lang_pick if lang_pick is not None else st.session_state.get("about_lang", "TR")
    if lang == "ENG":
        st.markdown(
            """
<div class="about-card">
  <p><strong>developer: cem evecen</strong></p>
  <div class="about-grid">
    <div class="about-kpi"><span>input channels</span><strong>store link · file · text · compare</strong></div>
    <div class="about-kpi"><span>analysis modes</span><strong>fast (heuristic) · rich (llm)</strong></div>
    <div class="about-kpi"><span>outputs</span><strong>dashboard · review cards · csv/excel/pdf</strong></div>
  </div>
  <p>
    This platform reads thousands of app reviews in one place and turns them into a clear picture of what users actually feel.
    Fast mode gives a quick and consistent sentiment read using simple rules; Rich mode uses an AI model to better understand tone, context and nuance.
    You can follow the overall trend and still open each individual review to see the exact words behind every number.
  </p>
  <div class="about-table-wrap">
    <table class="about-table">
      <thead>
        <tr><th>stage</th><th>what happens</th><th>result</th></tr>
      </thead>
      <tbody>
        <tr><td>1. collect</td><td>reviews are fetched from selected source and normalized</td><td>clean input pool</td></tr>
        <tr><td>2. filter</td><td>duplicates and low-signal entries are removed</td><td>analysis-ready dataset</td></tr>
        <tr><td>3. score</td><td>heuristic or llm pipeline runs sentiment and context extraction</td><td>structured sentiment rows</td></tr>
        <tr><td>4. summarize</td><td>metrics, distributions, and app-level comparisons are aggregated</td><td>actionable product view</td></tr>
        <tr><td>5. export</td><td>raw and analyzed outputs are generated for reporting</td><td>csv, excel, pdf files</td></tr>
      </tbody>
    </table>
  </div>
  <div class="about-table-wrap">
    <table class="about-table">
      <thead>
        <tr><th>capability</th><th>scope</th></tr>
      </thead>
      <tbody>
        <tr><td>single-app analysis</td><td>sentiment quality view for one product timeline</td></tr>
        <tr><td>compare mode</td><td>same-window benchmark for two apps with aligned settings</td></tr>
        <tr><td>operational exports</td><td>supports sharing with product, support, and ops teams</td></tr>
      </tbody>
    </table>
  </div>
</div>
""",
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            """
<div class="about-card">
  <p><strong>geliştiren: cem evecen</strong></p>
  <div class="about-grid">
    <div class="about-kpi"><span>girdi kanalları</span><strong>mağaza linki · dosya · metin · karşılaştırma</strong></div>
    <div class="about-kpi"><span>analiz modları</span><strong>hızlı (heuristic) · zengin (llm)</strong></div>
    <div class="about-kpi"><span>çıktılar</span><strong>dashboard · yorum kartları · csv/excel/pdf</strong></div>
  </div>
  <p>
    Bu platform, binlerce uygulama yorumunu tek ekranda toplar ve kullanıcıların aslında ne hissettiğini anlaşılır bir özete çevirir.
    Hızlı mod basit kurallarla çalışır; yorumları saniyeler içinde olumlu, olumsuz ve nötr olarak ayırıp genel tabloyu gösterir.
    Zengin mod bir yapay zekâ modeli kullanır; cümlenin tonunu, bağlamını ve ince ayrıntılarını daha iyi yorumlar.
    Genel eğilimi tek bakışta görebilir, istediğin yorumu tek tek açıp hangi cümlenin hangi sonucu ürettiğini kontrol edebilirsin.
  </p>
  <div class="about-table-wrap">
    <table class="about-table">
      <thead>
        <tr><th>aşama</th><th>ne olur</th><th>çıktı</th></tr>
      </thead>
      <tbody>
        <tr><td>1. toplama</td><td>yorumlar seçilen kaynaktan alınır ve normalize edilir</td><td>temiz giriş havuzu</td></tr>
        <tr><td>2. filtreleme</td><td>tekrarlı ve düşük sinyalli kayıtlar ayıklanır</td><td>analize hazır veri seti</td></tr>
        <tr><td>3. skorlama</td><td>heuristic veya llm hattı duygu ve bağlam analizi yapar</td><td>yapısal duygu satırları</td></tr>
        <tr><td>4. özetleme</td><td>metrikler, dağılımlar ve uygulama bazlı kıyaslar üretilir</td><td>aksiyon alınabilir ürün görünümü</td></tr>
        <tr><td>5. dışa aktarma</td><td>ham ve analizlenmiş çıktılar raporlama için hazırlanır</td><td>csv, excel, pdf dosyaları</td></tr>
      </tbody>
    </table>
  </div>
  <div class="about-table-wrap">
    <table class="about-table">
      <thead>
        <tr><th>özellik</th><th>kapsam</th></tr>
      </thead>
      <tbody>
        <tr><td>tek uygulama analizi</td><td>tek ürün için duygu kalitesi ve trend görünümü</td></tr>
        <tr><td>karşılaştırma modu</td><td>iki uygulamayı aynı zaman penceresinde hizalı kıyaslama</td></tr>
        <tr><td>operasyonel raporlama</td><td>ürün, destek ve operasyon ekipleriyle paylaşılabilir çıktı</td></tr>
      </tbody>
    </table>
  </div>
</div>
""",
            unsafe_allow_html=True,
        )


def main() -> None:
    ensure_branding_assets()
    _fav = favicon_abs_path()
    st.set_page_config(
        page_title="hakkında · ai store review analysis",
        layout="wide",
        initial_sidebar_state="collapsed",
        page_icon=_fav if _fav else None,
    )
    _inject_css()
    render_masthead(on_about=True)
    _render_about_body()


main()
