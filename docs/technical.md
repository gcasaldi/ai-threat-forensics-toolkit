# Technical details

Questo documento raccoglie i dettagli tecnici avanzati che sono stati rimossi dal README principale.

1) Struttura package

- `src/ai_threat_forensics_toolkit/core/` : scorer euristico (implementazione principale)
- `src/ai_threat_forensics_toolkit/ai/` : moduli ML opzionali (training, inferenza)

2) Modulo ML

- `ai_threat_forensics_toolkit.ai.model` offre:
  - estrazione features (riusa il scorer euristico)
  - generatori di dati sintetici
  - funzioni di training e salvataggio modello (`joblib`)
  - `compute_url_risk_with_ai` per blending euristico + modello

3) Notebook

- `notebooks/01-explore-and-train.ipynb` contiene un flusso di esempio per generare dati, esplorare feature, allenare e salvare un modello.

4) Valutazione

- `scripts/evaluate_model.py` esegue cross-validation con metriche standard (precision/recall/f1/roc_auc) e salva report in `reports/`.

5) Script utili

- `scripts/generate_synthetic_data.py` — salva `data/synthetic.csv`.
- `scripts/train_model.py` — allena e salva `models/url_risk_model.joblib`.
- `scripts/triage_from_file.py` — esempio di triage CSV per use-case operativo.

6) Testing & CI

- Test pytest di base in `tests/`.
- CI: `.github/workflows/ci.yml` esegue installazione editable, test e ruff.

7) Note per produzione

- Raccogliere dataset reale etichettato e definire policy di release e privacy.
- Aggiungere monitoraggio delle metriche di inferenza e drift.
- Introdurre pipeline di training riproducibile con salvataggio di metadata (config, seed, dataset hash).
