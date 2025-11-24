from pathlib import Path
import sys

# Ensure the package `src/` is importable during pytest collection
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
