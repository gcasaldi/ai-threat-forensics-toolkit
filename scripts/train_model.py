"""Train a model on synthetic data and save it to `models/url_risk_model.joblib`.

Usage:
    python scripts/train_model.py
"""
from pathlib import Path
from ai_threat_forensics_toolkit.ai.model import train_model_on_synthetic_data


def main():
    models = Path("models")
    models.mkdir(exist_ok=True)
    model = train_model_on_synthetic_data(n_samples=1000, model_path=models / "url_risk_model.joblib")
    print("Saved model to", models / "url_risk_model.joblib")


if __name__ == "__main__":
    main()
