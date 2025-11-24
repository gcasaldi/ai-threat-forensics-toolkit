# ai-threat-forensics-toolkit — Project Definition

## Elevator Pitch
Toolkit leggero per il triage automatico e spiegabile di URL (e indicatori correlati). Fornisce uno scorer euristico come fallback e moduli ML opzionali per migliorare priorità e automazione in SOC/DFIR.

## Visione
Diventare uno strumento affidabile, trasparente e riproducibile per ridurre i tempi di triage e aiutare analisti e strumenti automatizzati a prioritizzare incidenti.

## Missione
- Fornire scoring URL spiegabile e riproducibile.
- Offrire script CLI e notebook per prototipazione e valutazione ML.
- Consentire un percorso chiaro da prototipo a pipeline riproducibile.

## Cosa fa oggi
- Scorer euristico spiegabile (`ai_threat_forensics_toolkit.core.url_risk_scorer`).
- Modulo ML opzionale per esperimenti (`ai_threat_forensics_toolkit.ai.model`).
- Script batch per triage (`scripts/triage_from_file.py`) che genera CSV pronti per analisti.
- Notebook e script per generare dati sintetici, allenare e valutare modelli.
- Test automatici e CI di base (pytest + ruff).

## Scope
**In-scope**
- Scoring URL euristico e ML opzionale
- CLI per batch → CSV
- Notebook di esperimenti, script di training e valutazione
- Test automatici e CI

**Out-of-scope (per ora)**
- Integrazioni SIEM complesse out-of-the-box
- Inference orchestration a scala completa
- Raccolta/annotazione di dataset reali sensibili

## Utenti target
Analisti SOC/DFIR, ricercatori/engineer che prototipano scoring di indicatori, team che vogliono un fallback euristico spiegabile.

## Requisiti non funzionali
- Performance: batch scoring parallelo (joblib) con target throughput da definire
- Sicurezza: non committare segreti; usare `.env.example` e secret manager
- Reproducibilità: notebook + script + versioning modello (joblib)
- Observability: logging strutturato e possibilità di upload artifacts in CI

## Metriche di successo
- CI verde (tests + lint) su `main`
- Output triage d'esempio incluso (`reports/example_triage.csv`)
- Tempo medio per URL (benchmark) sotto soglia definita
- Documentazione minima: `README.md`, `docs/technical.md`, `CONTRIBUTING.md`

## Roadmap sintetica
- v0.1: scorer euristico, CLI batch, tests, README conciso, CI, esempio CSV
- v0.2: packaging (wheel), Docker image, benchmark, CHANGELOG, CONTRIBUTING
- v1.0: ML su dati reali + ML lifecycle (DVC/MLflow), endpoint di inference, monitoraggio

## Deliverables v0.1
- `README.md` conciso
- `docs/technical.md`
- Tests passing + CI
- `scripts/triage_from_file.py` + `reports/example_triage.csv`
- Tag `v0.1` e `CHANGELOG.md` (da creare)

## Governance
- Licenza: MIT
- Contributi: usare pre-commit, test e CI; aggiungere `CONTRIBUTING.md` per dettagli

---

Per procedere: posso committare questo file e creare il tag `v0.1` o aggiungere `CHANGELOG.md` e `CONTRIBUTING.md` ora. Dimmi come preferisci procedere.