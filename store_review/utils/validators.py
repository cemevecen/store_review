from __future__ import annotations

import re
from typing import Any


def is_valid_comment(text: Any) -> bool:
    """
    Filter pasted metadata, developer replies, and noise lines
    (Play / App Store exports, Connect copy-pastes).
    """
    if not text:
        return False
    s = str(text).strip()
    sl = s.lower()

    if len(s) < 3:
        return False
    if sl in ("nan", "null", "none"):
        return False

    meta_keywords = [
        "developer response",
        "geliştirici cevabı",
        "developer answer",
        "customer review",
        "müşteri yorumu",
        "app store connect",
        "review details",
        "yorum detayları",
        "version:",
        "versiyon:",
        "report a concern",
        "rapor et",
        "reply",
        "cevapla",
        "edit response",
        "cevabı düzenle",
    ]
    if any(k in sl for k in meta_keywords):
        return False

    if re.search(r"version\s+\d+(\.\d+)*", sl):
        return False

    months = [
        "jan",
        "feb",
        "mar",
        "apr",
        "may",
        "jun",
        "jul",
        "aug",
        "sep",
        "oct",
        "nov",
        "dec",
        "ocak",
        "şubat",
        "mart",
        "nisan",
        "mayıs",
        "haziran",
        "temmuz",
        "ağustos",
        "eylül",
        "ekim",
        "kasım",
        "aralık",
    ]
    first_word = sl.split()[0].replace(".", "").replace(",", "") if sl.split() else ""
    if first_word in months and len(s) < 60:
        return False

    if len(s) < 45:
        date_regex = (
            r"(\d{1,4}[-./]\d{1,2}[-./]\d{1,4})|"
            r"((Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec|"
            r"Ocak|Şubat|Mart|Nisan|Mayıs|Haziran|Temmuz|Ağustos|Eylül|Ekim|Kasım|Aralık)\s+\d{1,2},?\s+\d{4})"
        )
        if re.search(date_regex, s, re.IGNORECASE):
            return False

    formal_patterns = [
        "aksaklık için üzgünüz",
        "yaşanan aksaklık için",
        "teşekkür ederiz. yaşadığınız",
        "teşekkürler. yaşadığınız",
        "good day, thank you for the feedback",
        "support team",
        "destek ekibi",
        "iletişime geçtiğiniz için teşekkür",
        "bize ulaştığınız için teşekkür",
        "ilgili birimlerimize iletiyoruz",
        "çözüm için çalışıyoruz",
        "güncelleme ile giderilmiştir",
        "versiyonda giderilmiştir",
        "sorununuz devam ediyorsa",
        "yeni versiyon yayınlandı",
        "yükleyebilmiş miydiniz",
        "yardıma ihtiyacınız olursa",
        "iyi günler dileriz",
    ]
    if any(fp in sl for fp in formal_patterns):
        return False

    if re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", sl):
        return False

    return True
