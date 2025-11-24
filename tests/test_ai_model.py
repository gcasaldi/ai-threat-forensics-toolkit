import pytest

sklearn = pytest.importorskip("sklearn")

from ai_threat_forensics_toolkit.ai.model import (
    generate_synthetic_dataset,
    train_model_from_data,
    predict_proba,
    compute_url_risk_with_ai,
)


def test_train_and_predict_small():
    X, y = generate_synthetic_dataset(100)
    model = train_model_from_data(X, y)
    prob = predict_proba("http://login.example.xyz/reset", model)
    assert 0.0 <= prob <= 1.0


def test_compute_url_risk_with_ai_returns_result():
    X, y = generate_synthetic_dataset(100)
    model = train_model_from_data(X, y)
    res = compute_url_risk_with_ai("http://login.example.xyz/reset", model=model)
    assert hasattr(res, "score") and hasattr(res, "verdict")
