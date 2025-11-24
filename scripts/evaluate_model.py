"""Evaluate a trained model (or train-on-the-fly) with cross-validation.

Produces a JSON and CSV report under `reports/` and prints summary to stdout.

Usage:
    python scripts/evaluate_model.py [--model models/url_risk_model.joblib] [--n-samples 1000]
"""
from __future__ import annotations

import argparse
from pathlib import Path
import json
import csv

from ai_threat_forensics_toolkit.ai.model import (
    generate_synthetic_dataset,
    train_model_from_data,
    load_model,
    save_model,
)


def evaluate_model(model, X, y, cv=5):
    try:
        from sklearn.model_selection import cross_validate
        from sklearn.metrics import make_scorer, precision_score, recall_score, f1_score, roc_auc_score
    except Exception as exc:
        raise RuntimeError("scikit-learn is required to run evaluation") from exc

    scoring = {
        "precision": make_scorer(precision_score),
        "recall": make_scorer(recall_score),
        "f1": make_scorer(f1_score),
        "roc_auc": "roc_auc",
    }

    res = cross_validate(model, X, y, cv=cv, scoring=scoring, return_train_score=False)
    # compute mean/std
    summary = {}
    for k, v in res.items():
        summary[k] = {"mean": float((sum(v) / len(v)) if len(v) else 0.0), "std": float((__import__('statistics').stdev(v) if len(v) > 1 else 0.0))}

    return summary


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", type=str, default="models/url_risk_model.joblib", help="Path to model (joblib)")
    parser.add_argument("--n-samples", type=int, default=1000, help="Number of synthetic samples if training on the fly")
    parser.add_argument("--cv", type=int, default=5, help="Cross-validation folds")
    args = parser.parse_args()

    reports_dir = Path("reports")
    reports_dir.mkdir(exist_ok=True)

    # Load or train model
    model_path = Path(args.model)
    if model_path.exists():
        model = load_model(model_path)
        print(f"Loaded model from {model_path}")
    else:
        print("No model found, training a fresh model on synthetic data...")
        X, y = generate_synthetic_dataset(args.n_samples)
        model = train_model_from_data(X, y)
        save_model(model, model_path)
        print(f"Trained and saved model to {model_path}")

    # ensure we have X,y for evaluation
    X, y = generate_synthetic_dataset(args.n_samples)

    summary = evaluate_model(model, X, y, cv=args.cv)

    report = {
        "model_path": str(model_path),
        "n_samples": args.n_samples,
        "cv": args.cv,
        "summary": summary,
    }

    json_path = reports_dir / "evaluation_report.json"
    csv_path = reports_dir / "evaluation_report.csv"

    with open(json_path, "w") as fh:
        json.dump(report, fh, indent=2)

    # Flatten for CSV
    rows = []
    for metric, vals in summary.items():
        rows.append({"metric": metric, "mean": vals["mean"], "std": vals["std"]})

    with open(csv_path, "w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=["metric", "mean", "std"])
        writer.writeheader()
        for r in rows:
            writer.writerow(r)

    print("Evaluation summary:")
    for metric, vals in summary.items():
        print(f" - {metric}: mean={vals['mean']:.4f}, std={vals['std']:.4f}")

    print(f"Saved JSON report to {json_path}")
    print(f"Saved CSV report to {csv_path}")


if __name__ == "__main__":
    main()
