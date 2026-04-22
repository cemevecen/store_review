"""
Analiz edilmiş yorumları tek sütunlu kart listesi olarak gösterir (çok sütunlu tablo yok).
"""

from __future__ import annotations

import html
from typing import Any

import pandas as pd
import streamlit as st


def _format_tr_date(val: Any) -> str:
    if val is None or val == "":
        return "—"
    if isinstance(val, float) and pd.isna(val):
        return "—"
    if hasattr(val, "strftime"):
        try:
            return val.strftime("%d-%m-%Y")
        except Exception:
            pass
    s = str(val).strip()
    if not s:
        return "—"
    try:
        return pd.to_datetime(s).strftime("%d-%m-%Y")
    except Exception:
        return s[:48]


def _sentiment_dot_color(verdict: str) -> str:
    v = (verdict or "").strip()
    if v == "Olumlu":
        return "#22c55e"
    if v == "Olumsuz":
        return "#ef4444"
    if v == "İstek/Görüş":
        return "#3b82f6"
    return "#94a3b8"


def _one_card_html(row: dict[str, Any], fallback_index: int) -> str:
    no = row.get("No")
    try:
        n = int(no) if no is not None else fallback_index + 1
    except (TypeError, ValueError):
        n = fallback_index + 1
    verdict = str(row.get("Baskın Duygu", "") or "").strip()
    dot = _sentiment_dot_color(verdict)
    puan_raw = row.get("Puan", "—")
    if puan_raw is None or (isinstance(puan_raw, float) and pd.isna(puan_raw)):
        puan_s = "—"
    else:
        puan_s = html.escape(str(puan_raw).strip() or "—")
    tarih_disp = html.escape(_format_tr_date(row.get("Tarih")))
    body = str(row.get("Yorum", row.get("text", "")) or "")
    body_e = html.escape(body)
    app = row.get("Uygulama")
    app_block = ""
    if app is not None and str(app).strip():
        app_block = f'<div class="review-card-app">{html.escape(str(app).strip())}</div>'

    return (
        f'<div class="review-card">'
        f"{app_block}"
        f'<div class="review-card-head">'
        f'<span class="review-card-head-left">'
        f'<span class="review-card-no">#{n}</span>'
        f'<span class="review-card-sep">|</span>'
        f'<span class="review-card-dot" style="background:{dot};" title="{html.escape(verdict or "—")}"></span>'
        f'<span class="review-card-sep">|</span>'
        f'<span>Puan: {puan_s}</span>'
        f"</span>"
        f'<span class="review-card-date">Tarih: {tarih_disp}</span>'
        f"</div>"
        f'<div class="review-card-body">{body_e}</div>'
        f"</div>"
    )


def render_analyzed_review_cards(rows: list[dict[str, Any]], *, key_prefix: str = "cards") -> None:
    """Analiz satırlarını (No, Yorum, Baskın Duygu, Puan, Tarih, …) kart listesi olarak basar."""
    if not rows:
        return
    inner = "".join(_one_card_html(r, i) for i, r in enumerate(rows))
    st.markdown(
        f'<div class="review-card-list" data-cards="{html.escape(key_prefix)}">{inner}</div>',
        unsafe_allow_html=True,
    )
