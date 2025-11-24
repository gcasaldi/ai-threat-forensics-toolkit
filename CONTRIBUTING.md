# Contributing

Grazie per l'interesse a contribuire a ai-threat-forensics-toolkit! Ecco alcune linee guida rapide per collaborare efficacemente.

1. Apri un issue prima di iniziare a lavorare su feature importanti o cambi architetturali.
2. Fork & branch: crea un branch con nome `feat/descrizione` o `fix/descrizione`.
3. Formatta il codice e controlla gli errori locali:

```bash
pip install -r requirements-dev.txt
# esegui i controlli locali
python -m ruff check .
pytest -q
```

4. Usa i `pre-commit` hooks prima di committare (sono già configurati nel repository):

```bash
pre-commit install
pre-commit run --all-files
```

5. Tests: aggiungi test unitari per nuove funzionalità e assicurati che la suite sia verde.
6. Documentazione: aggiorna `docs/technical.md` o `README.md` per cambiare comportamento o API.
7. Security: non committare segreti; aggiungi `.env` a `.gitignore` e usa secret manager per CI.
8. Pull request: apri PR verso `main` con descrizione chiara, link a issue correlati e changelog proposto.

Grazie — le revisioni saranno eseguite via PR e merge dopo approvazione e CI verde.
