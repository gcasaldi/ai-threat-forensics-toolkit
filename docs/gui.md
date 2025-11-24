# GUI — URL Triage

Questa pagina descrive la piccola GUI inclusa nel progetto per eseguire il triage batch di URL.

File principale
- `scripts/gui.py` — applicazione Tkinter leggera che permette di:
  - caricare un file di URL (uno per riga)
  - eseguire lo scoring (parallelizzato con `joblib` se disponibile)
  - visualizzare i risultati in una tabella e salvarli in CSV

Quick start

```bash
# assicurati di avere le dipendenze di sviluppo
pip install -r requirements-dev.txt
# avvia la GUI
python scripts/gui.py
```

Notes
- La GUI è intenzionalmente minimale: è pensata per uso locale/analista come helper rapido.
- Non salva le chiavi/API in alcun file; se il tuo workflow richiede chiavi, impostale come env var prima di lanciare la GUI.
- Se `pandas` o `joblib` non sono disponibili, la GUI effettua un fallback sequenziale e utilizza scrittura CSV di base.

Suggerimenti per miglioramenti futuri
- Aggiungere una vista dei dettagli (breakdown delle feature) per ogni URL usando i `details` restituiti dallo scorer.
- Aggiungere un'opzione per caricare un modello ML salvato e usare il punteggio misto (euristico + ML).
- Esportare report HTML con grafici riassuntivi.
