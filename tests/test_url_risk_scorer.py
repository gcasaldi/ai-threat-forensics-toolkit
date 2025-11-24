from pathlib import Path
import importlib.util

# Load the implementation directly from the source file so tests don't
# depend on sys.path/package resolution in different environments.
module_path = Path(__file__).resolve().parent.parent / "src" / "ai_threat_forensics_toolkit" / "core" / "url_risk_scorer.py"
spec = importlib.util.spec_from_file_location("url_risk_scorer", str(module_path))
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
compute_url_risk = module.compute_url_risk


def test_compute_url_risk_basic():
    res = compute_url_risk("https://www.example.com")
    assert res.url == "https://www.example.com"
    assert isinstance(res.score, float)
    assert res.verdict in {"Low", "Medium", "High"}


def test_compute_url_risk_suspicious_keywords_and_http():
    # contains suspicious keywords and uses http
    url = "http://login-update-account.example.xyz/reset"
    res = compute_url_risk(url)
    # Expect some keyword hits and an http penalty
    assert res.details["keyword_score"] >= 10
    assert res.details["https_penalty"] == 20
    assert res.score > 30
