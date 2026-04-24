"""
Analiz sonuçları — nlp-sentiment-project ile uyumlu kart + iki sütun + özet düzeni.
"""

from __future__ import annotations

import html
import random
from collections import Counter
from collections import defaultdict

import pandas as pd
import plotly.express as px
import streamlit as st

from store_review.config.i18n import t as _t


def _counts(df: pd.DataFrame) -> tuple[int, int, int, int]:
    analysis_df = df[df["Baskın Duygu"] != "—"].copy()
    vc = analysis_df["Baskın Duygu"].value_counts()
    m_pos = int(vc.get("Olumlu", 0))
    m_neg = int(vc.get("Olumsuz", 0))
    m_neu = int(vc.get("İstek/Görüş", 0))
    return m_pos, m_neg, m_neu, len(df)


def _arc_pct(pct: float, circ: float) -> tuple[float, float]:
    filled = round(circ * pct / 100, 1)
    gap = round(circ - filled, 1)
    return filled, gap


def _sample_texts(rows: list[dict], verdict: str, n: int = 2, max_len: int = 140) -> list[str]:
    texts = [str(r.get("Yorum", "")).strip() for r in rows if r.get("Baskın Duygu") == verdict and str(r.get("Yorum", "")).strip()]
    if not texts:
        return []
    pick = texts if len(texts) <= n else random.sample(texts, n)
    out = []
    for t in pick:
        t = t.replace("\n", " ")
        if len(t) > max_len:
            t = t[: max_len - 1] + "…"
        out.append(html.escape(t))
    return out


def _render_concentric_legend(m_olumlu: int, m_olumsuz: int, m_istek: int) -> None:
    total_for_chart = m_olumlu + m_olumsuz + m_istek or 1
    pos_pct = int((m_olumlu / total_for_chart) * 100)
    neg_pct = int((m_olumsuz / total_for_chart) * 100)
    neu_pct = max(0, 100 - pos_pct - neg_pct)

    r_outer, r_mid, r_inner = 54, 38, 22
    c_outer = 2 * 3.14159 * r_outer
    c_mid = 2 * 3.14159 * r_mid
    c_inner = 2 * 3.14159 * r_inner

    pf, pg = _arc_pct(pos_pct, c_outer)
    nf, ng = _arc_pct(neg_pct, c_mid)
    uf, ug = _arc_pct(neu_pct, c_inner)

    st.markdown(
        f"""
        <div class="sr-responsive-row" style="display:flex;align-items:center;gap:20px;padding:8px 0 4px 0;">
            <svg width="140" height="140" viewBox="0 0 140 140" style="flex-shrink:0;">
                <circle cx="70" cy="70" r="{r_outer}" fill="none" stroke="#E2E8F0" stroke-width="10"/>
                <circle cx="70" cy="70" r="{r_mid}" fill="none" stroke="#E2E8F0" stroke-width="10"/>
                <circle cx="70" cy="70" r="{r_inner}" fill="none" stroke="#E2E8F0" stroke-width="10"/>
                <circle cx="70" cy="70" r="{r_outer}" fill="none" stroke="#10b981" stroke-width="10"
                    stroke-linecap="round" stroke-dasharray="{pf} {pg}" transform="rotate(-90 70 70)"/>
                <circle cx="70" cy="70" r="{r_mid}" fill="none" stroke="#f43f5e" stroke-width="10"
                    stroke-linecap="round" stroke-dasharray="{nf} {ng}" transform="rotate(-90 70 70)"/>
                <circle cx="70" cy="70" r="{r_inner}" fill="none" stroke="#818cf8" stroke-width="10"
                    stroke-linecap="round" stroke-dasharray="{uf} {ug}" transform="rotate(-90 70 70)"/>
                <text x="70" y="75" text-anchor="middle"
                    style="font-size:14px;font-weight:700;fill:#1E293B;font-family:Poppins,sans-serif;">
                    {pos_pct}%
                </text>
            </svg>
            <div style="display:flex;flex-direction:column;gap:10px;">
                <div style="display:flex;align-items:center;gap:8px;">
                    <div style="width:28px;height:4px;border-radius:2px;background:#10b981;"></div>
                    <div>
                        <div style="font-size:0.9rem;font-weight:700;color:#10b981;line-height:1.2;">{pos_pct}%</div>
                        <div style="font-size:0.7rem;color:#94A3B8;font-weight:600;">{html.escape(_t("dash.sent_pos"))}</div>
                    </div>
                </div>
                <div style="display:flex;align-items:center;gap:8px;">
                    <div style="width:28px;height:4px;border-radius:2px;background:#f43f5e;"></div>
                    <div>
                        <div style="font-size:0.9rem;font-weight:700;color:#f43f5e;line-height:1.2;">{neg_pct}%</div>
                        <div style="font-size:0.7rem;color:#94A3B8;font-weight:600;">{html.escape(_t("dash.sent_neg"))}</div>
                    </div>
                </div>
                <div style="display:flex;align-items:center;gap:8px;">
                    <div style="width:28px;height:4px;border-radius:2px;background:#818cf8;"></div>
                    <div>
                        <div style="font-size:0.9rem;font-weight:700;color:#818cf8;line-height:1.2;">{neu_pct}%</div>
                        <div style="font-size:0.7rem;color:#94A3B8;font-weight:600;">{html.escape(_t("dash.sent_req"))}</div>
                    </div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_experience_score(m_olumlu: int, m_olumsuz: int, m_istek: int) -> None:
    total_valid = m_olumlu + m_olumsuz + m_istek
    if total_valid <= 0:
        return
    score = int(((m_olumlu * 100) + (m_istek * 50)) / total_valid)
    score_color = "#10b981" if score >= 70 else "#f59e0b" if score >= 40 else "#f43f5e"
    st.markdown(
        f"""
        <div style="background-color:#FFFFFF;border:1px solid #E2E8F0;border-radius:12px;padding:15px;
                    margin-top:4px;margin-bottom:12px;text-align:center;box-shadow:0 4px 6px rgba(0,0,0,0.02);">
            <div style="font-size:0.85rem;color:#64748B;font-weight:700;margin-bottom:5px;text-transform:uppercase;letter-spacing:1px;">{html.escape(_t("dash.exp_score"))}</div>
            <div style="font-size:2.5rem;font-weight:800;color:{score_color};line-height:1;">{score}<span style="font-size:1.2rem;color:#94A3B8;">/100</span></div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_trend(rows: list[dict]) -> None:
    try:
        dated = [r for r in rows if r.get("Tarih") and r.get("Baskın Duygu") != "—"]
        if len(dated) < 20:
            return
        dated_sorted = sorted(dated, key=lambda x: x["Tarih"])
        half = len(dated_sorted) // 2
        first_half = dated_sorted[:half]
        second_half = dated_sorted[half:]

        def neg_rate(lst: list) -> float:
            if not lst:
                return 0.0
            return sum(1 for r in lst if r["Baskın Duygu"] == "Olumsuz") / len(lst)

        r1 = neg_rate(first_half)
        r2 = neg_rate(second_half)
        diff_trend = r2 - r1
        if diff_trend > 0.05:
            trend_icon, trend_color, trend_text = "↑", "#f43f5e", f"Olumsuz oran artıyor (+%{int(diff_trend * 100)})"
        elif diff_trend < -0.05:
            trend_icon, trend_color, trend_text = "↓", "#10b981", f"Memnuniyet artıyor (+%{int(abs(diff_trend) * 100)})"
        else:
            trend_icon, trend_color, trend_text = "→", "#f59e0b", "Oran stabil seyrediyor"
        st.markdown(
            f"""
            <div class="sr-responsive-row" style="background:#FFFFFF;border:1px solid #E2E8F0;border-radius:12px;padding:12px 15px;margin-top:8px;display:flex;align-items:center;gap:10px;">
                <span style="font-size:1.6rem;color:{trend_color};font-weight:800;line-height:1;">{trend_icon}</span>
                <div>
                    <div style="font-size:0.7rem;color:#94A3B8;font-weight:700;text-transform:uppercase;letter-spacing:1px;">{html.escape(_t("dash.trend"))}</div>
                    <div style="font-size:0.85rem;font-weight:600;color:{trend_color};">{html.escape(trend_text)}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    except Exception:
        pass


def _render_daily_negative(rows: list[dict]) -> None:
    try:
        dated2 = [r for r in rows if r.get("Tarih") and r.get("Baskın Duygu") != "—"]
        if len(dated2) < 14:
            return
        day_neg: defaultdict[str, int] = defaultdict(int)
        day_total: defaultdict[str, int] = defaultdict(int)
        for r in dated2:
            try:
                d = pd.to_datetime(r["Tarih"]).strftime("%a")
                day_total[d] += 1
                if r["Baskın Duygu"] == "Olumsuz":
                    day_neg[d] += 1
            except Exception:
                pass
        days_order = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        days_tr = {"Mon": "Pzt", "Tue": "Sal", "Wed": "Çrş", "Thu": "Per", "Fri": "Cum", "Sat": "Cmt", "Sun": "Paz"}
        cells = ""
        for d in days_order:
            if day_total[d] == 0:
                continue
            rate = day_neg[d] / day_total[d]
            bg = "#FEE2E2" if rate >= 0.6 else ("#FEF9C3" if rate >= 0.35 else "#DCFCE7")
            fc = "#DC2626" if rate >= 0.6 else ("#D97706" if rate >= 0.35 else "#16A34A")
            cells += (
                f'<div style="flex:1;text-align:center;background:{bg};border-radius:8px;padding:6px 2px;">'
                f'<div style="font-size:0.65rem;color:{fc};font-weight:700;">{days_tr[d]}</div>'
                f'<div style="font-size:0.7rem;color:{fc};font-weight:600;">%{int(rate * 100)}</div>'
                f"</div>"
            )
        if cells:
            st.markdown(
                f"""
                <div style="background:#FFFFFF;border:1px solid #E2E8F0;border-radius:12px;padding:12px 15px;margin-top:8px;">
                    <div style="font-size:0.7rem;color:#94A3B8;font-weight:700;text-transform:uppercase;letter-spacing:1px;margin-bottom:8px;">{html.escape(_t("dash.daily_neg"))}</div>
                    <div class="sr-week-dow-strip" style="display:flex;gap:4px;">{cells}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
    except Exception:
        pass


def _render_sentiment_summary(
    rows: list[dict],
    m_olumlu: int,
    m_olumsuz: int,
    m_istek: int,
    total_all: int,
    use_fast: bool,
) -> None:
    st.markdown(f"### {_t('dash.sent_dist')}")

    if total_all == 0:
        st.markdown(
            f"""
<div style="background:#F8FAFC;border-radius:12px;padding:20px 24px;border:1px solid #E2E8F0;">
    <div style="font-size:0.9rem;color:#64748b;">{html.escape(_t("dash.no_data_yet"))}</div>
</div>
""",
            unsafe_allow_html=True,
        )
        return

    pos_l = [r for r in rows if r.get("Baskın Duygu") == "Olumlu"]
    neg_l = [r for r in rows if r.get("Baskın Duygu") == "Olumsuz"]

    pos_p = int(len(pos_l) / total_all * 100) if total_all else 0
    neg_p = int(len(neg_l) / total_all * 100) if total_all else 0

    if pos_p >= 55:
        summary_title = "Topluluk Genel Olarak Olumlu"
        tone_intro = f"Analiz edilen {total_all} yorumun %{pos_p}'ü olumlu. Kullanıcılar genel olarak deneyimlerinden memnun."
    elif neg_p >= 50:
        summary_title = "Dikkat çeken olumsuz bir eğilim"
        tone_intro = f"Yorumların %{neg_p}'si olumsuz. Teknik sorunlar veya kullanım zorlukları öne çıkıyor."
    else:
        summary_title = "Dengeli kullanıcı deneyimi"
        tone_intro = f"Yorumlar olumlu (%{pos_p}) ve olumsuz (%{neg_p}) arasında dengeli bir dağılım sergiliyor."

    pos_s = _sample_texts(rows, "Olumlu", 2)
    neg_s = _sample_texts(rows, "Olumsuz", 2)
    pos_part = f"Öne çıkan ifadeler: {'; '.join(pos_s)}." if pos_s else ""
    neg_part = f"Olumsuz örnekler: {'; '.join(neg_s)}." if neg_s else ""
    summary_body = f"{html.escape(tone_intro)} {pos_part} {neg_part}".strip()

    all_v = [str(r.get("Versiyon", "")).strip() for r in rows if r.get("Versiyon") and str(r.get("Versiyon")).strip() not in ("", "—")]
    top_v = Counter(all_v).most_common(1)
    best_v = html.escape(top_v[0][0]) if top_v else "Belirlenemedi"
    all_lang = [str(r.get("lang", "tr")).upper() for r in rows]
    top_l = Counter(all_lang).most_common(1)
    best_l = html.escape(top_l[0][0]) if top_l else "TR"

    subtitle = (
        "Hızlı analiz özeti"
        if use_fast
        else "Zengin analiz — özet"
    )
    quote_color = "#818cf8" if use_fast else "#7c3aed"
    title_color = "#6366F1" if use_fast else "#5b21b6"

    persona_html = f"""
<div style="margin-top:16px;padding:12px;background:#eff6ff;border-radius:10px;border:1px solid #dbeafe;">
    <div style="font-size:0.75rem;font-weight:700;color:#3b82f6;text-transform:uppercase;margin-bottom:4px;">{html.escape(_t("dash.persona"))}</div>
    <div style="font-size:0.85rem;color:#1e40af;line-height:1.5;">
        • <b>En yoğun sürüm / kanal:</b> {best_v}<br>
        • <b>Hakim dil etiketi:</b> {best_l}<br>
        • <b>Not:</b> Örnek yorumlar yukarıda kısaltılmıştır.
    </div>
</div>"""

    st.markdown(
        f"""
<div style="background:#F8FAFC;border-radius:12px;padding:20px 24px;position:relative;border:1px solid #E2E8F0;">
    <div style="font-size:0.75rem;font-weight:600;color:#64748b;margin-bottom:6px;">{html.escape(subtitle)}</div>
    <div style="font-size:52px;line-height:0.6;color:{quote_color};font-family:Georgia,serif;opacity:0.35;margin-bottom:10px;user-select:none;">"</div>
    <div style="font-size:0.82rem;font-weight:700;color:{title_color};text-transform:uppercase;letter-spacing:1px;margin-bottom:8px;">{html.escape(summary_title)}</div>
    <div style="font-size:0.9rem;color:#1E293B;line-height:1.75;margin:0;">{summary_body}</div>
    {persona_html}
    <div class="sr-summary-footer" style="margin-top:18px;padding-top:12px;border-top:1px solid #E2E8F0;display:flex;gap:12px;align-items:center;">
        <div style="display:flex;gap:4px;">
            <div style="width:8px;height:8px;border-radius:50%;background:#10b981;"></div>
            <div style="width:8px;height:8px;border-radius:50%;background:#f43f5e;"></div>
            <div style="width:8px;height:8px;border-radius:50%;background:#818cf8;"></div>
        </div>
        <span style="font-size:0.7rem;color:#94A3B8;font-weight:500;">{m_olumlu} olumlu · {m_olumsuz} olumsuz · {m_istek} görüş analiz edildi</span>
    </div>
</div>
""",
        unsafe_allow_html=True,
    )


def _render_puan_distribution(df: pd.DataFrame) -> None:
    if "Puan" not in df.columns or not df["Puan"].notna().any():
        return
    st.markdown("---")
    st.markdown(f"### {_t('dash.score_dist')}")
    freq = st.radio(
        "Zaman ölçeği",
        ["Günlük", "Haftalık", "Aylık"],
        horizontal=True,
        label_visibility="collapsed",
        key="sr_puan_freq_sel",
    )
    df_puan = df.dropna(subset=["Tarih", "Puan"]).copy()
    try:
        df_puan["Puan_val"] = pd.to_numeric(df_puan["Puan"], errors="coerce").fillna(0).astype(int)
        df_puan = df_puan[(df_puan["Puan_val"] >= 1) & (df_puan["Puan_val"] <= 5)]
    except Exception:
        return
    if df_puan.empty:
        st.caption("Tarih ve puan bilgisi olan yorum yok.")
        return

    df_puan["Tarih_dt"] = pd.to_datetime(df_puan["Tarih"])
    min_d = df_puan["Tarih_dt"].min().strftime("%d-%m-%Y")
    max_d = df_puan["Tarih_dt"].max().strftime("%d-%m-%Y")
    st.caption(f"**Tespit Edilen Tarih Aralığı:** {min_d} ile {max_d}")

    tr_months = {
        1: "Ocak",
        2: "Şubat",
        3: "Mart",
        4: "Nisan",
        5: "Mayıs",
        6: "Haziran",
        7: "Temmuz",
        8: "Ağustos",
        9: "Eylül",
        10: "Ekim",
        11: "Kasım",
        12: "Aralık",
    }

    if freq == "Haftalık":
        df_puan["Grup"] = df_puan["Tarih_dt"].dt.to_period("W").apply(lambda r: r.start_time)
        df_puan["Grup_Label"] = df_puan["Grup"].apply(lambda x: f"{x.day} {tr_months[x.month]} {x.year}")
        title_txt = "Haftalık Puan Dağılımı"
    elif freq == "Aylık":
        df_puan["Grup_Label"] = df_puan["Tarih_dt"].apply(lambda x: f"{tr_months[x.month]} {x.year}")
        df_puan["Grup"] = df_puan["Tarih_dt"].dt.to_period("M").apply(lambda r: r.start_time)
        title_txt = "Aylık Puan Dağılımı"
    else:
        df_puan["Grup_Label"] = df_puan["Tarih_dt"].dt.strftime("%d-%m-%Y")
        df_puan["Grup"] = df_puan["Tarih_dt"].dt.date
        title_txt = "Günlük Puan Dağılımı"

    dist_trend = df_puan.groupby(["Grup", "Grup_Label", "Puan_val"]).size().reset_index(name="Oy Sayısı")
    dist_trend["Puan_Label"] = dist_trend["Puan_val"].apply(lambda x: f"{x} Yıldız")
    dist_trend = dist_trend.sort_values(["Grup", "Puan_val"], ascending=[True, True])
    _sorted_dates = dist_trend["Grup_Label"].unique().tolist()

    fig_dist = px.bar(
        dist_trend,
        x="Grup_Label",
        y="Oy Sayısı",
        color="Puan_Label",
        title=title_txt,
        color_discrete_map={
            "1 Yıldız": "#E53E3E",
            "2 Yıldız": "#F6AD55",
            "3 Yıldız": "#F6E05E",
            "4 Yıldız": "#68D391",
            "5 Yıldız": "#2F855A",
        },
        category_orders={
            "Puan_Label": ["1 Yıldız", "2 Yıldız", "3 Yıldız", "4 Yıldız", "5 Yıldız"],
            "Grup_Label": _sorted_dates,
        },
        labels={"Puan_Label": "", "Grup_Label": "Zaman", "Oy Sayısı": "Sayı"},
    )
    fig_dist.update_layout(
        height=420,
        margin={"t": 60, "b": 100, "l": 10, "r": 10},
        xaxis_title="",
        yaxis_title="Yorum / Puan Sayısı",
        legend={
            "orientation": "h",
            "yanchor": "bottom",
            "y": 1.02,
            "xanchor": "right",
            "x": 1,
            "font": {"color": "#0f172a"},
        },
        barmode="stack",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(248,250,252,0.6)",
        font=dict(color="#334155"),
    )
    fig_dist.update_xaxes(tickangle=-45)
    st.plotly_chart(fig_dist, use_container_width=True)


def render_analysis_results_dashboard(rows: list[dict], *, use_fast: bool = True) -> None:
    """nlp-sentiment tarzı özet paneli: metrik hapları, sol göstergeler, sağ metin özeti, isteğe bağlı puan grafiği."""
    if not rows:
        return
    df = pd.DataFrame(rows)
    if df.empty or "Baskın Duygu" not in df.columns:
        st.info(_t("dash.missing_cols"))
        return

    m_olumlu, m_olumsuz, m_istek, n_total = _counts(df)
    total_all = m_olumlu + m_olumsuz + m_istek

    st.markdown(
        f'<h2 class="sr-analysis-page-title">{html.escape(_t("dash.page_title"))}</h2>',
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
    <div class="sr-analysis-metric-row">
        <div class="sr-analysis-metric-pill">
            <div class="sr-analysis-metric-value" style="color:#10b981;">{m_olumlu}</div>
            <div class="sr-analysis-metric-label">Olumlu</div>
        </div>
        <div class="sr-analysis-metric-pill">
            <div class="sr-analysis-metric-value" style="color:#f43f5e;">{m_olumsuz}</div>
            <div class="sr-analysis-metric-label">Olumsuz</div>
        </div>
        <div class="sr-analysis-metric-pill">
            <div class="sr-analysis-metric-value" style="color:#3b82f6;">{m_istek}</div>
            <div class="sr-analysis-metric-label">İstek / Görüş</div>
        </div>
        <div class="sr-analysis-metric-pill">
            <div class="sr-analysis-metric-value" style="color:#a78bfa;">{n_total}</div>
            <div class="sr-analysis-metric-label">Toplam Veri</div>
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    col_pie, col_summary = st.columns([1, 1], gap="medium")
    with col_pie:
        _render_concentric_legend(m_olumlu, m_olumsuz, m_istek)
        _render_experience_score(m_olumlu, m_olumsuz, m_istek)
        _render_trend(rows)
        _render_daily_negative(rows)

    with col_summary:
        _render_sentiment_summary(rows, m_olumlu, m_olumsuz, m_istek, total_all, use_fast)

    _render_puan_distribution(df)
