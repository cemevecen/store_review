"""
Türkçe (UTF-8) duyarlı PDF üretimi — Noto Sans TTF ile tam glif desteği (ğ, ü, ş, ı, ö, ç, İ).
"""

from __future__ import annotations

import io
import re
from datetime import datetime
from pathlib import Path
from typing import Any

import pandas as pd

_FONT_PATH = Path(__file__).resolve().parent.parent / "data" / "fonts" / "NotoSans-Regular.ttf"

_ANALYSIS_COL_ORDER = (
    "No",
    "Uygulama",
    "Yorum",
    "Baskın Duygu",
    "Olumlu %",
    "İstek/Görüş %",
    "Olumsuz %",
    "Tarih",
    "Puan",
    "Versiyon",
    "lang",
    "Yöntem",
)


def _ensure_font() -> Path:
    if not _FONT_PATH.is_file():
        raise FileNotFoundError(
            f"PDF font eksik: {_FONT_PATH}. NotoSans-Regular.ttf veri klasörüne ekleyin."
        )
    return _FONT_PATH


def _cell_text(x: Any) -> str:
    if x is None:
        return ""
    if isinstance(x, float) and pd.isna(x):
        return ""
    s = str(x).replace("\r\n", "\n").replace("\r", "\n")
    if len(s) > 12000:
        s = s[:12000] + "…"
    return s


def _ordered_columns(df: pd.DataFrame) -> list[str]:
    seen: list[str] = []
    for c in _ANALYSIS_COL_ORDER:
        if c in df.columns and c not in seen:
            seen.append(c)
    for c in df.columns:
        if c not in seen:
            seen.append(c)
    return seen


def build_analysis_pdf_bytes(rows: list[dict[str, Any]], *, source_label: str) -> bytes:
    """Analiz sonuç tablosu (satır listesi) → PDF baytları."""
    from fpdf import FPDF  # PyPI: fpdf2

    if not rows:
        raise ValueError("rows boş olamaz")
    font = _ensure_font()
    df = pd.DataFrame(rows)
    cols = _ordered_columns(df)

    pdf = FPDF(orientation="L", unit="mm", format="A4")
    pdf.set_auto_page_break(auto=True, margin=14)
    pdf.set_margins(14, 14, 14)
    pdf.add_font("NotoSans", "", str(font))
    pdf.add_page()
    pdf.set_font("NotoSans", "", 11)

    pdf.set_title("duygu analizi sonuç raporu")
    pdf.set_creator("store_review")
    pdf.set_subject("UTF-8 / Türkçe")

    w = pdf.epw
    pdf.set_font("NotoSans", "", 14)
    pdf.multi_cell(w, 8, "duygu analizi sonuç raporu")
    pdf.set_font("NotoSans", "", 10)
    pdf.multi_cell(w, 6, f"kaynak: {_cell_text(source_label)}")
    pdf.multi_cell(w, 6, f"oluşturulma: {datetime.now():%Y-%m-%d %H:%M}")
    pdf.multi_cell(w, 6, f"satır sayısı: {len(df)}")
    if "Baskın Duygu" in df.columns:
        vc = df["Baskın Duygu"].fillna("—").astype(str).value_counts()
        oz = " · ".join(f"{k}: {int(v)}" for k, v in vc.items())
        pdf.multi_cell(w, 6, f"duygu dağılımı: {oz}")
    pdf.ln(4)

    pdf.set_font("NotoSans", "", 9)
    for i in range(len(df)):
        row = df.iloc[i]
        pdf.set_font("NotoSans", "", 10)
        pdf.multi_cell(w, 6, f"— satır {i + 1} —")
        pdf.set_font("NotoSans", "", 8.5)
        for c in cols:
            val = _cell_text(row.get(c))
            label = str(c)
            pdf.multi_cell(w, 5, f"{label}: {val}")
        pdf.ln(2)

    out = io.BytesIO()
    pdf.output(out)
    return out.getvalue()


def build_raw_pool_pdf_bytes(rows: list[dict[str, Any]], *, source_label: str) -> bytes:
    """Ham havuz (analiz öncesi) yorumları → PDF."""
    from fpdf import FPDF  # PyPI: fpdf2

    if not rows:
        raise ValueError("rows boş olamaz")
    font = _ensure_font()
    df = pd.DataFrame(rows)
    cols = list(df.columns)

    pdf = FPDF(orientation="L", unit="mm", format="A4")
    pdf.set_auto_page_break(auto=True, margin=14)
    pdf.set_margins(14, 14, 14)
    pdf.add_font("NotoSans", "", str(font))
    pdf.add_page()
    pdf.set_font("NotoSans", "", 11)
    pdf.set_title("yorum havuzu (ham)")
    pdf.set_creator("store_review")

    w = pdf.epw
    pdf.set_font("NotoSans", "", 14)
    pdf.multi_cell(w, 8, "yorum havuzu (analiz öncesi)")
    pdf.set_font("NotoSans", "", 10)
    pdf.multi_cell(w, 6, f"kaynak: {_cell_text(source_label)}")
    pdf.multi_cell(w, 6, f"oluşturulma: {datetime.now():%Y-%m-%d %H:%M}")
    pdf.multi_cell(w, 6, f"kayıt: {len(df)}")
    pdf.ln(3)

    for i in range(len(df)):
        row = df.iloc[i]
        pdf.set_font("NotoSans", "", 10)
        pdf.multi_cell(w, 6, f"— kayıt {i + 1} —")
        pdf.set_font("NotoSans", "", 8.5)
        for c in cols:
            pdf.multi_cell(w, 5, f"{c}: {_cell_text(row.get(c))}")
        pdf.ln(2)

    out = io.BytesIO()
    pdf.output(out)
    return out.getvalue()


def safe_pdf_filename(prefix: str) -> str:
    base = datetime.now().strftime("%Y%m%d_%H%M")
    pfx = re.sub(r"[^\w\-]+", "_", prefix.lower())[:32].strip("_") or "export"
    return f"{pfx}_{base}.pdf"
