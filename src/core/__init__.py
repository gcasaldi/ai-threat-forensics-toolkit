"""Compatibility shim for legacy `src.core` imports.

This project used to expose modules under `src.core`. The canonical package
is now `ai_threat_forensics_toolkit.core`. Importing `src.core` will raise an
informative ImportError to guide updating imports.
"""

raise ImportError(
	"Legacy package 'src.core' is removed. Use 'ai_threat_forensics_toolkit.core' instead."
)
