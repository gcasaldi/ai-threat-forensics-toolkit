"""Generate a small synthetic dataset for training experiments.

Usage:
    python scripts/generate_synthetic_data.py --out data/synthetic.csv
"""
from pathlib import Path
import csv
from ai_threat_forensics_toolkit.ai.model import generate_synthetic_dataset


def main():
    out = Path("data")
    out.mkdir(exist_ok=True)
    X, y = generate_synthetic_dataset(500)
    with open(out / "synthetic.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["length_score", "keyword_score", "dash_score", "https_penalty", "tld_score", "label"])
        for feats, lab in zip(X, y):
            w.writerow(list(feats) + [lab])


if __name__ == "__main__":
    main()
