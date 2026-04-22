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


PAGE_SIZE = 50
_MAX_PAGE_BUTTONS = 15


def _list_sig(rows: list[dict[str, Any]]) -> tuple[int, str, str]:
    n = len(rows)
    if n == 0:
        return (0, "", "")
    a = str(rows[0].get("Yorum", rows[0].get("text", "")))[:120]
    b = str(rows[-1].get("Yorum", rows[-1].get("text", "")))[:120]
    return (n, a, b)


def render_analyzed_review_cards(rows: list[dict[str, Any]], *, key_prefix: str = "cards") -> None:
    """Analiz satırlarını kart listesi olarak basar; 50'den fazlaysa sayfalama + Tümünü gör."""
    if not rows:
        return

    sig_k = f"{key_prefix}_review_list_sig"
    page_k = f"{key_prefix}_review_cards_page"
    show_all_k = f"{key_prefix}_review_cards_show_all"
    sig = _list_sig(rows)
    if st.session_state.get(sig_k) != sig:
        st.session_state[sig_k] = sig
        st.session_state[page_k] = 0
        st.session_state[show_all_k] = False

    n = len(rows)
    show_all = bool(st.session_state.get(show_all_k, False))

    if n <= PAGE_SIZE:
        slice_rows = rows
    elif show_all:
        slice_rows = rows
    else:
        page = int(st.session_state.get(page_k, 0))
        total_pages = max(1, (n + PAGE_SIZE - 1) // PAGE_SIZE)
        page = max(0, min(page, total_pages - 1))
        st.session_state[page_k] = page
        start = page * PAGE_SIZE
        slice_rows = rows[start : start + PAGE_SIZE]

    if n > PAGE_SIZE:
        if show_all:
            if st.button("50'şer göster", key=f"{key_prefix}_collapse_list"):
                st.session_state[show_all_k] = False
                st.session_state[page_k] = 0
                st.rerun()
        else:
            page = int(st.session_state.get(page_k, 0))
            total_pages = max(1, (n + PAGE_SIZE - 1) // PAGE_SIZE)
            start = page * PAGE_SIZE
            end = min(start + PAGE_SIZE, n)

            c_prev, c_info, c_next = st.columns([1, 3, 1])
            with c_prev:
                if st.button("Önceki", key=f"{key_prefix}_prev_page", disabled=page <= 0):
                    st.session_state[page_k] = page - 1
                    st.rerun()
            with c_info:
                st.caption(f"**{start + 1}–{end}** / {n} yorum · sayfa **{page + 1}** / **{total_pages}**")
            with c_next:
                if st.button("Sonraki", key=f"{key_prefix}_next_page", disabled=page >= total_pages - 1):
                    st.session_state[page_k] = page + 1
                    st.rerun()

            if total_pages <= _MAX_PAGE_BUTTONS:
                cols = st.columns(total_pages)
                for i in range(total_pages):
                    with cols[i]:
                        is_cur = i == page
                        if st.button(
                            str(i + 1),
                            key=f"{key_prefix}_pgnum_{i}",
                            type="primary" if is_cur else "secondary",
                            use_container_width=True,
                            disabled=is_cur,
                        ):
                            st.session_state[page_k] = i
                            st.rerun()
            else:
                st.caption(f"Çok sayfa ({total_pages}); **Önceki** / **Sonraki** ile gezinin.")

            if st.button("Tümünü gör", key=f"{key_prefix}_show_all_reviews", use_container_width=True):
                st.session_state[show_all_k] = True
                st.rerun()

    inner = "".join(_one_card_html(r, i) for i, r in enumerate(slice_rows))
    st.markdown(
        f'<div class="review-card-list" data-cards="{html.escape(key_prefix)}">{inner}</div>',
        unsafe_allow_html=True,
    )
