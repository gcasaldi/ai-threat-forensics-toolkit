"""Deprecated compatibility module.

The real implementation lives in ``src.core.url_risk_scorer``. Importing
this module will raise an informative ImportError to avoid accidental
usage of the old top-level module.
"""

raise ImportError(
	"The top-level module 'url_risk_scorer' was moved to 'src.core.url_risk_scorer'."
	" Please update your imports to 'from src.core.url_risk_scorer import ...'"
)
