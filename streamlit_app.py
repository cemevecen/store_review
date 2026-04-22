"""
Store Review Sentiment — capstone entry (Streamlit).

Run from project root:
  streamlit run streamlit_app.py
"""

from __future__ import annotations

import re
import sys
from datetime import datetime
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dotenv import load_dotenv

load_dotenv(ROOT / ".env", override=True)

from store_review.config.settings import Settings
from store_review.config.theme import APP_CSS
from store_review.core.ai_providers import DEFAULT_MODELS, RichAnalyzer, resolve_api_keys
from store_review.core.analyzer import analyze_batch, dedupe_reviews
from store_review.fetchers.app_store import get_app_store_reviews
from store_review.fetchers.file_loader import load_reviews_from_dataframe
from store_review.fetchers.google_play import fetch_google_play_reviews
from store_review.utils.exporters import df_to_csv_bytes, df_to_excel_bytes
from store_review.utils.validators import is_valid_comment


def _secrets_get(key: str):
    try:
        return st.secrets.get(key)
    except Exception:
        return None


def _parse_play_id(raw: str) -> str | None:
    s = raw.strip()
    m = re.search(r"id=([\w.]+)", s)
    if m:
        return m.group(1)
    if re.match(r"^[\w.]+$", s):
        return s
    return None


def _parse_ios_id(raw: str) -> str | None:
    s = raw.strip()
    m = re.search(r"id(\d{6,})", s, re.I)
    if m:
        return m.group(1)
    if re.match(r"^\d{6,}$", s):
        return s
    return None


def _prepare_pool(rows: list[dict]) -> list[dict]:
    out = []
    for r in dedupe_reviews(rows):
        t = str(r.get("text", "")).strip()
        if len(t) < 2:
            continue
        rr = dict(r)
        rr["is_valid"] = is_valid_comment(t)
        out.append(rr)
    return out


def _inject_css():
    st.markdown(f"<style>{APP_CSS}</style>", unsafe_allow_html=True)


def main():
    st.set_page_config(
        page_title="Mağaza Yorumu Analizi",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    _inject_css()

    st.markdown('<p class="header-title">Mağaza yorumu duygu analizi</p>', unsafe_allow_html=True)
    st.markdown(
        '<p class="header-sub">Google Play & App Store · Heuristic (ücretsiz) veya Gemini / Groq / OpenAI</p>',
        unsafe_allow_html=True,
    )

    env_settings = Settings.from_env()
    gk, gqk, ok = resolve_api_keys(
        env_settings.gemini_api_key,
        env_settings.groq_api_key,
        env_settings.openai_api_key,
        _secrets_get,
    )

    with st.sidebar:
        st.subheader("API durumu")
        st.write("Gemini:", "✓" if gk else "—")
        st.write("Groq:", "✓" if gqk else "—")
        st.write("OpenAI:", "✓" if ok else "—")
        st.caption(".env veya Streamlit secrets içinde anahtarları tanımlayın.")
        st.divider()
        st.markdown("**Zengin analiz** için en az bir anahtar gerekir.")

    if "review_pool" not in st.session_state:
        st.session_state.review_pool = []
    if "analysis_rows" not in st.session_state:
        st.session_state.analysis_rows = []

    tab_play, tab_ios, tab_file, tab_text = st.tabs(
        ["Google Play", "App Store", "Dosya yükle", "Metin yapıştır"]
    )

    with tab_play:
        st.text_input("Play package veya mağaza URL", key="play_input", placeholder="com.whatsapp veya ...id=com.whatsapp")
        d_play = st.number_input("Son X gün (Play)", min_value=1, max_value=365, value=30, key="play_days")
        if st.button("Play yorumlarını çek", key="btn_play"):
            pid = _parse_play_id(st.session_state.play_input)
            if not pid:
                st.error("Geçerli bir uygulama kimliği veya URL girin.")
            else:
                prog = st.progress(0.0)
                st.session_state.review_pool = fetch_google_play_reviews(
                    pid,
                    int(d_play),
                    _progress_callback=lambda x: prog.progress(min(float(x), 1.0)),
                )
                st.success(f"{len(st.session_state.review_pool)} benzersiz yorum yüklendi.")
                st.session_state.analysis_rows = []

    with tab_ios:
        st.text_input("App Store sayısal id veya URL", key="ios_input", placeholder="284882215 veya .../id284882215...")
        d_ios = st.number_input("Son X gün (iOS)", min_value=1, max_value=365, value=30, key="ios_days")
        if st.button("App Store yorumlarını çek", key="btn_ios"):
            aid = _parse_ios_id(st.session_state.ios_input)
            if not aid:
                st.error("Geçerli bir App Store id veya URL girin.")
            else:
                prog = st.progress(0.0)
                st.session_state.review_pool = get_app_store_reviews(
                    aid,
                    _progress_callback=lambda x: prog.progress(min(float(x), 1.0)),
                    _days_limit=int(d_ios),
                )
                st.success(f"{len(st.session_state.review_pool)} benzersiz yorum yüklendi.")
                st.session_state.analysis_rows = []

    with tab_file:
        up = st.file_uploader("CSV veya Excel", type=["csv", "xlsx"])
        if up:
            try:
                if up.name.lower().endswith(".csv"):
                    df = pd.read_csv(up)
                else:
                    df = pd.read_excel(up)
                st.session_state.review_pool = load_reviews_from_dataframe(df)
                st.success(f"{len(st.session_state.review_pool)} satır yüklendi (filtre sonrası).")
                st.session_state.analysis_rows = []
            except Exception as e:
                st.error(str(e))

    with tab_text:
        ta = st.text_area("Her satır bir yorum", height=200, key="paste_reviews")
        if st.button("Metni yükle", key="btn_paste"):
            lines = [ln.strip() for ln in ta.splitlines() if ln.strip()]
            pool = []
            for i, ln in enumerate(lines):
                if not is_valid_comment(ln):
                    continue
                pool.append(
                    {
                        "id": f"paste-{i}",
                        "text": ln,
                        "date": None,
                        "rating": "",
                        "lang": "paste",
                        "is_valid": True,
                    }
                )
            st.session_state.review_pool = pool
            st.success(f"{len(pool)} yorum hazır.")
            st.session_state.analysis_rows = []

    st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)

    pool = st.session_state.review_pool
    st.metric("Havuzdaki yorum", len(pool))

    if pool:
        raw_df = pd.DataFrame(pool)
        with st.expander("Ham veriyi indir"):
            c1, c2 = st.columns(2)
            with c1:
                st.download_button(
                    "CSV",
                    data=df_to_csv_bytes(raw_df),
                    file_name=f"reviews_raw_{datetime.now():%Y%m%d_%H%M}.csv",
                    mime="text/csv",
                )
            with c2:
                st.download_button(
                    "Excel",
                    data=df_to_excel_bytes(raw_df),
                    file_name=f"reviews_raw_{datetime.now():%Y%m%d_%H%M}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                )

    c_m1, c_m2, c_m3 = st.columns(3)
    with c_m1:
        method = st.radio("Analiz", ["Hızlı (heuristic)", "Zengin (LLM)"], horizontal=True)
    with c_m2:
        depth = st.radio("Derinlik", ["Standart", "Gelişmiş"], horizontal=True, disabled=(method == "Hızlı (heuristic)"))
    with c_m3:
        provider = st.selectbox(
            "Öncelikli sağlayıcı (Zengin)",
            ["Google Gemini", "Groq AI", "OpenAI"],
            disabled=(method == "Hızlı (heuristic)"),
        )

    model = st.text_input(
        "Model adı",
        value=DEFAULT_MODELS.get(provider, ""),
        disabled=(method == "Hızlı (heuristic)"),
        help="Sağlayıcıya göre varsayılanı kullanabilir veya kendi modelinizi yazabilirsiniz.",
    )

    use_fast = method == "Hızlı (heuristic)"
    mode_idx = 0 if depth == "Standart" else 1

    rich = RichAnalyzer(gemini_key=gk, groq_key=gqk, openai_key=ok)

    if st.button("Analizi başlat", type="primary"):
        prepared = _prepare_pool(pool)
        if not prepared:
            st.warning("Önce yorum yükleyin.")
        elif not use_fast and not (gk or gqk or ok):
            st.error("Zengin analiz için en az bir API anahtarı gerekir.")
        else:
            bar = st.progress(0.0)
            status = st.empty()

            def prog(done: int, total: int):
                bar.progress(done / max(total, 1))
                status.text(f"{done} / {total}")

            rows = analyze_batch(
                prepared,
                use_heuristic_only=use_fast,
                analysis_mode=mode_idx,
                rich=None if use_fast else rich,
                provider=provider,
                model=model.strip() or DEFAULT_MODELS[provider],
                max_workers=28 if use_fast else 12,
                progress=prog,
                max_rich_items=500,
            )
            st.session_state.analysis_rows = rows
            bar.empty()
            status.empty()
            st.success("Analiz tamamlandı.")

    rows = st.session_state.analysis_rows
    if rows:
        st.subheader("Sonuçlar")
        df = pd.DataFrame(rows)
        vc = df["Baskın Duygu"].value_counts()
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Toplam", len(df))
        for col, label in [(m2, "Olumlu"), (m3, "Olumsuz"), (m4, "İstek/Görüş")]:
            col.metric(label, int(vc.get(label, 0)))

        pie_df = vc.reset_index()
        pie_df.columns = ["duygu", "adet"]
        fig = px.pie(pie_df, names="duygu", values="adet", hole=0.45, color="duygu", color_discrete_map={
            "Olumlu": "#34D399",
            "Olumsuz": "#F87171",
            "İstek/Görüş": "#60A5FA",
            "—": "#94A3B8",
        })
        st.plotly_chart(fig, use_container_width=True)

        st.dataframe(df, use_container_width=True, height=420)

        out_df = df.drop(columns=["Tarih"], errors="ignore") if "Tarih" in df.columns else df
        st.download_button(
            "Sonuç CSV",
            data=df_to_csv_bytes(out_df),
            file_name=f"analiz_{datetime.now():%Y%m%d_%H%M}.csv",
            mime="text/csv",
        )


if __name__ == "__main__":
    main()
