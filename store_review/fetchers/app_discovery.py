"""
Mağaza uygulaması keşfi: Play arama (google-play-scraper) + App Store iTunes Search API.
Doğrudan paket / ID / ürün URL çözümleme (eski streamlit_app mantığından sadeleştirilmiş).
"""

from __future__ import annotations

import re
import urllib.parse
from dataclasses import dataclass
from typing import Any, List, Literal, Optional, Tuple

import requests

Platform = Literal["android", "ios"]


@dataclass
class ResolvedApp:
    platform: Platform
    app_id: str


def search_play_store(query: str, n_hits: int = 50) -> List[dict[str, Any]]:
    try:
        from google_play_scraper import search as play_search
    except ImportError:
        return []
    try:
        res = play_search(query.strip(), n_hits=n_hits, lang="tr", country="tr")
    except Exception:
        return []
    out: List[dict[str, Any]] = []
    for a in res or []:
        aid = a.get("appId")
        if not aid:
            continue
        icon = (a.get("icon") or "").strip()
        out.append(
            {
                "platform": "Android",
                "appId": aid,
                "title": (a.get("title") or "—")[:80],
                "icon": icon,
            }
        )
    return out


def search_app_store_itunes(query: str, country: str = "TR", limit: int = 50) -> List[dict[str, Any]]:
    try:
        r = requests.get(
            "https://itunes.apple.com/search",
            params={
                "term": query.strip(),
                "country": country,
                "media": "software",
                "entity": "software",
                "limit": limit,
                "lang": "tr_TR",
            },
            timeout=12,
        )
        if r.status_code != 200:
            return []
        data = r.json()
    except Exception:
        return []
    out: List[dict[str, Any]] = []
    for app in data.get("results", [])[:limit]:
        tid = app.get("trackId")
        if not tid:
            continue
        out.append(
            {
                "platform": "iOS",
                "appId": str(tid),
                "title": (app.get("trackCensoredName") or app.get("trackName") or "—")[:80],
                "icon": (app.get("artworkUrl512") or app.get("artworkUrl100") or "").strip(),
            }
        )
    return out


def _first_play_search_package(search_query: str) -> Optional[str]:
    try:
        from google_play_scraper import search as play_search

        hits = play_search(search_query.replace("+", " "), n_hits=1, lang="tr", country="tr")
        if hits:
            return str(hits[0].get("appId") or "")
    except Exception:
        pass
    try:
        q = urllib.parse.quote(search_query)
        url = f"https://play.google.com/store/search?q={q}&c=apps"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        r = requests.get(url, headers=headers, timeout=12)
        if r.status_code != 200:
            return None
        matches = re.findall(r"/store/apps/details\?id=([^\"&]+)", r.text)
        if matches:
            return matches[0]
    except Exception:
        return None
    return None


def _first_itunes_search_id(term: str, country: str = "tr") -> Optional[str]:
    try:
        r = requests.get(
            f"https://itunes.apple.com/search",
            params={"term": term, "entity": "software", "country": country, "limit": 5},
            timeout=10,
        )
        if r.status_code != 200:
            return None
        data = r.json()
        res = data.get("results") or []
        if res:
            return str(res[0].get("trackId", ""))
    except Exception:
        return None
    return None


def resolve_play_product_or_search_url(raw: str) -> Tuple[Optional[ResolvedApp], Optional[str]]:
    """
    play.google.com ürün veya arama linki → ResolvedApp veya bilgi mesajı.
    """
    u = raw.strip()
    if "play.google.com" not in u.lower():
        return None, None
    m = re.search(r"id=([^&/]+)", u)
    if m:
        return ResolvedApp("android", m.group(1)), None
    sm = re.search(r"[?&]q=([^&/]+)", u)
    if sm:
        q = urllib.parse.unquote_plus(sm.group(1))
        pkg = _first_play_search_package(q)
        if pkg:
            return ResolvedApp("android", pkg), f"Play arama linki çözüldü: “{q}” → ilk sonuç."
        return None, f"Play Store’da “{q}” için sonuç bulunamadı."
    return None, None


def resolve_apple_product_or_search_url(raw: str) -> Tuple[Optional[ResolvedApp], Optional[str]]:
    u = raw.strip()
    if "apple.com" not in u.lower() and "apps.apple.com" not in u.lower():
        return None, None
    m = re.search(r"id(\d+)", u, re.I)
    if m:
        return ResolvedApp("ios", m.group(1)), None
    sm = re.search(r"[?&]term=([^&/]+)", u)
    if sm:
        term = urllib.parse.unquote_plus(sm.group(1))
        country_m = re.search(r"apple\.com/([a-z]{2})/", u.lower())
        cc = (country_m.group(1) if country_m else "tr").upper()
        aid = _first_itunes_search_id(term, country=cc.lower())
        if aid:
            return ResolvedApp("ios", aid), f"App Store arama linki çözüldü: “{term}” → ilk sonuç."
        return None, f"App Store’da “{term}” için sonuç bulunamadı."
    return None, None


def resolve_direct_input(raw: str) -> Tuple[Optional[ResolvedApp], Optional[str]]:
    """
    Metin kutusundaki değer doğrudan paket / sayısal id / ürün URL ise döner.
    Arama kelimesi (belirsiz) için None döner — listeden seçim gerekir.
    """
    u = raw.strip()
    if not u:
        return None, None

    r1, msg1 = resolve_play_product_or_search_url(u)
    if r1:
        return r1, msg1
    r2, msg2 = resolve_apple_product_or_search_url(u)
    if r2:
        return r2, msg2

    low = u.lower()
    if low.startswith("id") and len(u) > 2 and u[2:].isdigit():
        return ResolvedApp("ios", u[2:]), None
    if u.isdigit() and len(u) >= 6:
        return ResolvedApp("ios", u), None
    if "." in u and re.match(r"^[a-zA-Z0-9._]+$", u, re.IGNORECASE):
        return ResolvedApp("android", u), None

    return None, None


def looks_like_search_keyword(q: str) -> bool:
    """Liste araması göstermek için uygun mu (URL / paket / saf rakam değil)."""
    s = q.strip()
    if len(s) < 2:
        return False
    if s.lower().startswith("http"):
        return False
    if resolve_direct_input(s)[0] is not None:
        return False
    return True
