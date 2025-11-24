#!/usr/bin/env python3
"""Small Tkinter GUI for batch-scoring URLs and exporting CSV results.

Usage: python scripts/gui.py

Dependencies: tkinter (builtin), pandas, joblib (optional), ai_threat_forensics_toolkit
"""

import threading
import pathlib
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

try:
    import pandas as pd
except Exception:  # pragma: no cover - UI relies on pandas
    pd = None

from ai_threat_forensics_toolkit.core.url_risk_scorer import compute_url_risk


class UrlTriageApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("AI Threat Forensics Toolkit — URL Triage")
        self.geometry("800x480")
        self._urls = []
        self._results = []

        self._build_ui()

    def _build_ui(self):
        frm = ttk.Frame(self)
        frm.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Controls
        ctrl = ttk.Frame(frm)
        ctrl.pack(fill=tk.X)

        btn_load = ttk.Button(ctrl, text="Load URLs...", command=self.load_urls)
        btn_load.pack(side=tk.LEFT)

        self.btn_score = ttk.Button(ctrl, text="Run Scoring", command=self.run_scoring, state=tk.DISABLED)
        self.btn_score.pack(side=tk.LEFT, padx=8)

        btn_save = ttk.Button(ctrl, text="Save CSV...", command=self.save_csv, state=tk.DISABLED)
        btn_save.pack(side=tk.LEFT)
        self._btn_save = btn_save

        # Treeview for results
        cols = ("url", "score", "verdict")
        tree = ttk.Treeview(frm, columns=cols, show="headings")
        for c in cols:
            tree.heading(c, text=c)
            tree.column(c, anchor=tk.W, width=300 if c == "url" else 100)
        tree.pack(fill=tk.BOTH, expand=True, pady=8)
        self._tree = tree

        # Status
        status = ttk.Label(self, text="Ready", anchor=tk.W)
        status.pack(fill=tk.X, side=tk.BOTTOM)
        self._status = status

    def load_urls(self):
        path = filedialog.askopenfilename(title="Open URLs file", filetypes=[("Text files", "*.txt"), ("All files", "*")])
        if not path:
            return
        p = pathlib.Path(path)
        try:
            lines = [l.strip() for l in p.read_text(encoding="utf-8").splitlines() if l.strip()]
        except Exception as e:
            messagebox.showerror("Error", f"Unable to read file: {e}")
            return
        self._urls = lines
        self._results = []
        self._tree.delete(*self._tree.get_children())
        self._status.config(text=f"Loaded {len(self._urls)} URLs")
        self.btn_score.config(state=tk.NORMAL)
        self._btn_save.config(state=tk.DISABLED)

    def run_scoring(self):
        if not self._urls:
            messagebox.showinfo("Info", "No URLs loaded")
            return
        self.btn_score.config(state=tk.DISABLED)
        self._status.config(text="Scoring...")

        # Run scoring in background thread to keep UI responsive
        t = threading.Thread(target=self._do_score)
        t.daemon = True
        t.start()

    def _do_score(self):
        results = []
        # Try to use joblib for parallelism if available
        try:
            from joblib import Parallel, delayed

            def score(u):
                r = compute_url_risk(u)
                return {"url": r.url, "score": r.score, "verdict": r.verdict}

            results = Parallel(n_jobs=-1)(delayed(score)(u) for u in self._urls)
        except Exception:
            # fallback sequential
            for u in self._urls:
                r = compute_url_risk(u)
                results.append({"url": r.url, "score": r.score, "verdict": r.verdict})

        self._results = results
        # update UI on main thread
        self.after(0, self._show_results)

    def _show_results(self):
        self._tree.delete(*self._tree.get_children())
        for r in self._results:
            self._tree.insert("", tk.END, values=(r["url"], f"{r["score"]:.1f}", r["verdict"]))
        self._status.config(text=f"Scoring completed — {len(self._results)} results")
        self._btn_save.config(state=tk.NORMAL)
        self.btn_score.config(state=tk.NORMAL)

    def save_csv(self):
        if not self._results:
            messagebox.showinfo("Info", "No results to save")
            return
        path = filedialog.asksaveasfilename(title="Save CSV", defaultextension=".csv", filetypes=[("CSV", "*.csv")])
        if not path:
            return
        try:
            # Try to use pandas for robust CSV writing
            if pd is not None:
                df = pd.DataFrame(self._results)
                df.to_csv(path, index=False)
            else:
                # simple fallback
                with open(path, "w", encoding="utf-8") as fh:
                    fh.write("url,score,verdict\n")
                    for r in self._results:
                        fh.write(f"{r['url']},{r['score']},{r['verdict']}\n")
        except Exception as e:
            messagebox.showerror("Error", f"Unable to save CSV: {e}")
            return
        messagebox.showinfo("Saved", f"Results saved to {path}")
        self._status.config(text=f"Results saved to {path}")


def main():
    app = UrlTriageApp()
    app.mainloop()


if __name__ == "__main__":
    main()
