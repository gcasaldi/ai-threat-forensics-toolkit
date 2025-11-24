"""Simple triage script: read URLs from a file, score them and write CSV output.

Usage:
    python scripts/triage_from_file.py input_urls.txt output.csv

Output columns: url,score,verdict
"""
from pathlib import Path
import csv
import sys

from ai_threat_forensics_toolkit.core.url_risk_scorer import compute_url_risk


def triage_file(input_path: Path, output_path: Path):
    urls = []
    with input_path.open() as fh:
        for line in fh:
            u = line.strip()
            if u:
                urls.append(u)

    rows = []
    for u in urls:
        res = compute_url_risk(u)
        rows.append((res.url, float(f"{res.score:.1f}"), res.verdict))

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(["url", "score", "verdict"])
        for r in rows:
            writer.writerow(r)


def main(argv):
    if len(argv) < 3:
        print("Usage: python scripts/triage_from_file.py input_urls.txt output.csv")
        return 2

    input_path = Path(argv[1])
    output_path = Path(argv[2])
    triage_file(input_path, output_path)
    print(f"Wrote triage to {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
