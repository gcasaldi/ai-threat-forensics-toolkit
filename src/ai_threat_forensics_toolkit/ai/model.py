"""Lightweight ML integration for URL risk scoring.

This module is optional: scikit-learn is an optional dependency and the
functions will raise informative errors if the package is not installed.

The approach:
- extract the same features used by the heuristic scorer;
- provide helpers to generate synthetic data and to train/save a model;
- provide prediction and a blended `compute_url_risk_with_ai` wrapper that
  combines heuristic score and model probability.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import List, Tuple, Optional
import random
from pathlib import Path
import joblib

from ai_threat_forensics_toolkit.core.url_risk_scorer import (
    compute_url_risk,
    UrlRiskResult,
)


def _extract_features(url: str) -> List[float]:
    """Return features in the same order as the heuristic components."""
    res = compute_url_risk(url)
    comps = res.details
    return [
        comps["length_score"],
        comps["keyword_score"],
        comps["dash_score"],
        comps["https_penalty"],
        comps["tld_score"],
    ]


def generate_synthetic_dataset(n: int = 200) -> Tuple[List[List[float]], List[int]]:
    """Create a small synthetic dataset for quick experiments.

    Labels are derived from the heuristic score with some noise.
    """
    keywords = ["login", "update", "secure", "account", "bank", "paypal"]
    tlds = [".com", ".ru", ".xyz", ".net"]

    X = []
    y = []
    for _ in range(n):
        # build a synthetic URL
        host_parts = []
        # sometimes include suspicious keywords
        if random.random() < 0.5:
            host_parts.append(random.choice(keywords))
        host_parts.append("example")
        if random.random() < 0.3:
            host_parts.append("secure")
        host = "-".join(host_parts)
        scheme = "http://" if random.random() < 0.4 else "https://"
        tld = random.choice(tlds)
        path = "/reset" if random.random() < 0.2 else "/"
        url = f"{scheme}{host}{tld}{path}"

        feats = _extract_features(url)
        score = sum(feats)
        # derive label with threshold and noise
        label = 1 if score + random.uniform(-10, 10) >= 50 else 0
        X.append(feats)
        y.append(label)

    return X, y


def _require_sklearn():
    try:
        import sklearn  # noqa: F401
    except Exception as exc:  # pragma: no cover - depends on env
        raise ImportError(
            "scikit-learn is required for AI functionality. Install with: `pip install scikit-learn joblib`"
        ) from exc


def train_model_from_data(X: List[List[float]], y: List[int]):
    """Train a small classifier and return it. Requires scikit-learn."""
    _require_sklearn()
    from sklearn.ensemble import RandomForestClassifier

    clf = RandomForestClassifier(n_estimators=50, random_state=42)
    clf.fit(X, y)
    return clf


def save_model(model, path: str | Path):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, str(path))


def load_model(path: str | Path):
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Model not found at {p}")
    return joblib.load(str(p))


def predict_proba(url: str, model) -> float:
    """Return probability for 'malicious' class (0..1)."""
    feats = _extract_features(url)
    proba = model.predict_proba([feats])[0]
    # assume class '1' is malicious if model was trained that way
    if len(proba) == 1:
        return float(proba[0])
    return float(proba[1])


def compute_url_risk_with_ai(url: str, model=None, model_path: Optional[str] = None) -> UrlRiskResult:
    """Compute a blended risk score using heuristic and model probability.

    If `model` is None and `model_path` is provided, try to load it. If neither
    available, fall back to the pure heuristic `compute_url_risk`.
    """
    heuristic = compute_url_risk(url)
    if model is None and model_path is not None:
        try:
            model = load_model(model_path)
        except Exception:
            model = None

    if model is None:
        return heuristic

    try:
        prob = predict_proba(url, model)
    except Exception:
        return heuristic

    # Blend heuristic score (0-100 approx) and model probability
    blended = 0.6 * heuristic.score + 0.4 * (prob * 100)

    if blended >= 70:
        verdict = "High"
    elif blended >= 40:
        verdict = "Medium"
    else:
        verdict = "Low"

    details = dict(heuristic.details)
    details.update({"ai_probability": prob, "blended_score": blended})

    return UrlRiskResult(url=url, score=blended, verdict=verdict, details=details)


def train_model_on_synthetic_data(n_samples: int = 500, model_path: Optional[str] = None):
    """Convenience: generate data, train model and optionally save it."""
    X, y = generate_synthetic_dataset(n_samples)
    model = train_model_from_data(X, y)
    if model_path:
        save_model(model, model_path)
    return model
