from dataclasses import dataclass
from typing import List, Dict

SUSPICIOUS_KEYWORDS = [
    "login", "verify", "update", "secure", "account",
    "paypal", "bank", "invoice", "reset", "password"
]

SUSPICIOUS_TLDS = [
    ".ru", ".cn", ".tk", ".top", ".xyz"
]


@dataclass
class UrlRiskResult:
    url: str
    score: float
    verdict: str
    details: Dict[str, float]


def _length_score(url: str) -> float:
    length = len(url)
    return min(length / 10, 30)


def _keyword_score(url: str, keywords: List[str]) -> float:
    url_low = url.lower()
    hits = sum(1 for k in keywords if k in url_low)
    return hits * 10


def _dash_score(url: str) -> float:
    dashes = url.count("-")
    return min(dashes * 5, 25)


def _https_score(url: str) -> float:
    if url.lower().startswith("https://"):
        return 0
    if url.lower().startswith("http://"):
        return 20
    return 0


def _tld_score(url: str, bad_tlds: List[str]) -> float:
    for tld in bad_tlds:
        if url.lower().endswith(tld):
            return 25
    return 0


def compute_url_risk(url: str) -> UrlRiskResult:
    components = {
        "length_score": _length_score(url),
        "keyword_score": _keyword_score(url, SUSPICIOUS_KEYWORDS),
        "dash_score": _dash_score(url),
        "https_penalty": _https_score(url),
        "tld_score": _tld_score(url, SUSPICIOUS_TLDS),
    }

    total_score = sum(components.values())

    if total_score >= 70:
        verdict = "High"
    elif total_score >= 40:
        verdict = "Medium"
        #
    else:
        verdict = "Low"

    return UrlRiskResult(
        url=url,
        score=total_score,
        verdict=verdict,
        details=components,
    )
