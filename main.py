from pathlib import Path
import sys

# Ensure the project's src directory is on sys.path so imports work when
# running this file as a script (keeps running the example easy during
# development). When installed, imports can be used without this.
sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from ai_threat_forensics_toolkit.core.url_risk_scorer import compute_url_risk

test_urls = [
    "http://login-paypal-security-check.example.com/update",
    "https://www.google.com",
    "http://secure-account-verification-update-login.xyz/reset"
]

for u in test_urls:
    res = compute_url_risk(u)
    print("URL:", res.url)
    print("Score:", res.score, "- Verdict:", res.verdict)
    print("Details:", res.details)
    print("-" * 60)
