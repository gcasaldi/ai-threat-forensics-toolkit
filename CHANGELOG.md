# Changelog

Tutte le modifiche rilevanti a questo progetto saranno documentate in questo file.

## [Unreleased]
- Preparazione alla release v0.1

## [0.1.0] - 2025-11-24
### Added
- Scorer euristico per URL (`ai_threat_forensics_toolkit.core.url_risk_scorer`).
- Script di triage batch (`scripts/triage_from_file.py`) e esempio CSV (`reports/example_triage.csv`).
- Notebook di sperimentazione (`notebooks/01-explore-and-train.ipynb`).
- Modulo ML opzionale per prototipi (`src/ai_threat_forensics_toolkit/ai/model.py`).
- Script per training e valutazione (`scripts/train_model.py`, `scripts/evaluate_model.py`).
- Test automatici (`tests/`) e CI (`.github/workflows/ci.yml`).
- Documentazione tecnica di base (`docs/technical.md`) e `PROJECT.md`.

### Changed
- Repository riorganizzato in layout `src/` e namespace `ai_threat_forensics_toolkit`.

### Notes
- Questa è una release iniziale focalizzata su prototipazione riproducibile e strumenti di triage.
