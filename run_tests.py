from pathlib import Path
import sys

# Lightweight test runner (works without pytest). It ensures `src/` is on
# sys.path and runs a couple of sanity checks for `compute_url_risk`.
sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from ai_threat_forensics_toolkit.core.url_risk_scorer import compute_url_risk


def main():
    print("Running lightweight tests...")
    res = compute_url_risk("https://www.example.com")
    assert res.url == "https://www.example.com"
    assert isinstance(res.score, float)

    url = "http://login-update-account.example.xyz/reset"
    res = compute_url_risk(url)
    assert res.details["keyword_score"] >= 10
    assert res.details["https_penalty"] == 20

    print("All lightweight tests passed.")


if __name__ == "__main__":
    main()
