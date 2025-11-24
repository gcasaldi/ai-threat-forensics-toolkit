**Visione**: fornire strumenti pratici e spiegabili per il triage automatico degli indicatori di compromissione (in particolare URL), con possibilità di estendere il toolkit con moduli ML quando necessario.

## Quick start

1. Clona e installa in editable mode:

```bash
git clone <repo-url>
cd ai-threat-forensics-toolkit
pip install -e .
```

2. Esegui l'esempio rapido:

```bash
python main.py
```

3. (Opzionale) Per esperimenti e notebook:

```bash
pip install -r requirements-dev.txt
jupyter lab
# apri notebooks/01-explore-and-train.ipynb
```

## Feature attuali

- Scorer euristico spiegabile (`ai_threat_forensics_toolkit.core.url_risk_scorer`).
- Modulo ML opzionale per esperimenti (`ai_threat_forensics_toolkit.ai.model`).
- Notebook di prototipazione, script di training e valutazione, test base e CI.

## Roadmap (reale vs. futura)

**v0.1 (attuale)**
- Scorer euristico; notebook e script per esperimenti; test e CI.

**v0.2 (pianificato)**
- Valutazione automatica e report in CI; feature engineering avanzata; API di inferenza base.

**v1.0 (obiettivo)**
- Modello addestrato su dati reali; endpoint di inferenza robusto; policy privacy e monitoraggio.

## Esempio pratico (triage URL da email phishing)

Input: file `data/example_urls.txt` (URL per riga).

Comando:

```bash
python scripts/triage_from_file.py data/example_urls.txt reports/example_triage.csv
```

Esempio output (`reports/example_triage.csv`):

```
url,score,verdict
http://login-paypal-security-check.example.com/update,70.3,High
https://www.google.com,2.2,Low
http://secure-account-verification-update-login.xyz/reset,95.7,High
```

## Dettagli tecnici avanzati

Per i dettagli tecnici, notebook e script avanzati: `docs/technical.md`.

## Licenza

MIT — vedi `LICENSE`.