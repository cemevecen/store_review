"""Metin (paste) sekmesi için akıllı ayrıştırıcı.

Kullanıcı Excel/Google Sheets/CSV dışa aktarımından kopyala-yapıştır yaptığında
içerik çoğunlukla tab (Excel default) veya virgülle ayrılmış tablodur. Bu modül:

1. Girdinin tablosal olup olmadığını sezgisel olarak tespit eder.
2. Eğer tabloysa `pandas` ile okuyup mevcut `load_reviews_from_dataframe`
   yolundan geçirir (aynı sütun keşif mantığı: yorum/review/text/mesaj...).
3. Tablo değilse düz metin olarak satır-bazı ayrıştırmaya düşer.

Böylece "metni havuza yükle" akışında çok satırlı Excel verisi geldiğinde,
gerçek yorum sayısı (satırlara bölünmüş parçalar değil) elde edilir.
"""

from __future__ import annotations

import io
from typing import Any

import pandas as pd

from store_review.fetchers.file_loader import load_reviews_from_dataframe
from store_review.utils.validators import is_valid_comment


_TEXT_COL_HINTS = (
    "yorum",
    "review",
    "comment",
    "text",
    "content",
    "body",
    "mesaj",
)


def _has_text_like_column(df: pd.DataFrame) -> bool:
    cols = [str(c).strip().lower() for c in df.columns]
    for c in cols:
        if any(h in c for h in _TEXT_COL_HINTS):
            return True
    return False


def _try_read(text: str, sep: str) -> pd.DataFrame | None:
    """pandas ile denemeli okuma: hata/boş/çok-az-sütun halinde None."""
    try:
        df = pd.read_csv(
            io.StringIO(text),
            sep=sep,
            engine="python",
            dtype=str,
            keep_default_na=False,
            skip_blank_lines=True,
            on_bad_lines="skip",
        )
    except Exception:
        return None
    if df.empty or df.shape[1] < 2:
        return None
    return df


def _fallback_line_pool(text: str) -> list[dict[str, Any]]:
    """Tablo olarak okunamazsa: her satırı tek yorum kabul et."""
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    pool: list[dict[str, Any]] = []
    j = 0
    for ln in lines:
        if not is_valid_comment(ln):
            continue
        pool.append(
            {
                "id": f"paste-{j}",
                "text": ln,
                "date": None,
                "rating": "",
                "lang": "paste",
                "is_valid": True,
            }
        )
        j += 1
    return pool


def parse_pasted_reviews(text: str) -> list[dict[str, Any]]:
    """Yapıştırılmış metni yorum listesine çevirir.

    Önce Excel-kopyala formatı (TSV), sonra CSV denenir; ikisi de tablosal ve
    içinde yorum sütunu varsa `load_reviews_from_dataframe` ile normalize edilir.
    Aksi halde satır-bazına düşer.
    """
    if not isinstance(text, str) or not text.strip():
        return []

    for sep in ("\t", ","):
        df = _try_read(text, sep=sep)
        if df is None:
            continue
        if not _has_text_like_column(df):
            continue
        try:
            return load_reviews_from_dataframe(df)
        except Exception:
            continue

    return _fallback_line_pool(text)
