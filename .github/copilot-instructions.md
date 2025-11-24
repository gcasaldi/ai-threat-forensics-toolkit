# Copilot Instructions: AI Threat Forensics Toolkit

## Project Overview
Lightweight toolkit for explainable URL risk scoring and triage automation. Provides a heuristic-based scorer as the foundation, with optional ML modules for experimentation. Designed for SOC/DFIR analysts who need transparent, reproducible threat prioritization.

**Core Philosophy**: Heuristics first, ML optional. Everything must be explainable and reproducible.

## Architecture

### Module Structure
```
src/ai_threat_forensics_toolkit/
  core/url_risk_scorer.py    # Heuristic scorer (no external deps)
  ai/model.py                # Optional ML layer (requires scikit-learn)
scripts/                      # CLI tools for analysts
  triage_from_file.py        # Batch scoring → CSV output
  train_model.py             # ML training
  evaluate_model.py          # Model evaluation
```

**Key Design**: `core.url_risk_scorer` has zero external dependencies. ML functionality in `ai.model` is strictly optional and gracefully degrades with informative errors if scikit-learn isn't installed.

### Scoring Flow
1. URL → `compute_url_risk()` → returns `UrlRiskResult` dataclass
2. Score breakdown stored in `details` dict (length, keywords, dashes, http penalty, TLD)
3. Thresholds: ≥70 = High, ≥40 = Medium, <40 = Low
4. ML integration (optional): `compute_url_risk_with_ai()` blends heuristic + model probability

## Development Workflows

### Running Tests
```bash
# Quick validation (no pytest needed)
python run_tests.py

# Full suite with pytest
pip install -r requirements-dev.txt
pytest -v

# CI uses: ruff check . && pytest -q
```

### Adding Features
1. **Heuristic scorer changes**: Edit `src/ai_threat_forensics_toolkit/core/url_risk_scorer.py`
   - Keep functions pure (no side effects)
   - Update `compute_url_risk()` to modify score components
   - Add corresponding tests in `tests/test_url_risk_scorer.py`
   
2. **ML features**: Edit `src/ai_threat_forensics_toolkit/ai/model.py`
   - Always check dependencies with `_require_sklearn()`
   - Extract features via `_extract_features()` to match heuristic components
   - Synthetic data generation: `generate_synthetic_dataset()`

### Batch Triage Workflow
Analysts use this pattern:
```bash
# Input: data/example_urls.txt (one URL per line)
python scripts/triage_from_file.py data/example_urls.txt reports/output.csv
# Output: CSV with columns: url,score,verdict
```

## Project Conventions

### Import Patterns
```python
# Main entry point and scripts use sys.path.insert for development ease
sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))
from ai_threat_forensics_toolkit.core.url_risk_scorer import compute_url_risk

# Tests load directly via importlib.util to avoid sys.path issues
```

### Testing Philosophy
- Tests must work without installed package (development mode friendly)
- Use `importlib.util.spec_from_file_location` in test files
- Lightweight runner (`run_tests.py`) for environments without pytest
- Full suite via pytest for CI

### Code Style
- Line length: 88 chars (Black-compatible)
- Use dataclasses for structured outputs (`UrlRiskResult`)
- Type hints where helpful (not enforced strictly)
- Ruff for linting: `python -m ruff check .`

## Critical Files

- `src/ai_threat_forensics_toolkit/core/url_risk_scorer.py`: Core heuristic logic
- `scripts/triage_from_file.py`: Primary analyst workflow
- `main.py`: Quick validation/demo script
- `pyproject.toml`: Package config, ruff settings
- `requirements-dev.txt`: Development dependencies (pytest, jupyter, scikit-learn)

## Common Tasks

**Add a new heuristic component:**
1. Create `_new_score(url: str) -> float` function
2. Add to `components` dict in `compute_url_risk()`
3. Add test coverage in `tests/test_url_risk_scorer.py`

**Train model on real data:**
1. Prepare `X` (features) and `y` (labels) lists
2. Use `train_model_from_data(X, y)` from `ai.model`
3. Save with `save_model(model, "models/model_name.joblib")`

**Generate example reports:**
```bash
python scripts/triage_from_file.py data/example_urls.txt reports/example_triage.csv
```

## Gotchas

- **Import errors in tests**: Tests use `importlib.util` to load modules directly, not package imports
- **ML dependencies**: Never assume scikit-learn is installed; use `_require_sklearn()` guard
- **Path handling**: Scripts create parent directories automatically (`Path.mkdir(parents=True, exist_ok=True)`)
- **CSV output**: Always use `newline=""` parameter with `csv.writer()` for cross-platform compatibility
