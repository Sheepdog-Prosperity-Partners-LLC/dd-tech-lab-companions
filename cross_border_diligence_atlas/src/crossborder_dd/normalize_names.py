"""Name and identifier normalization helpers.

These helpers support triage matching. They do not prove identity.
"""

from __future__ import annotations

import re
import unicodedata


def normalize_name(value: object) -> str:
    """Return a conservative normalized name for triage matching."""
    if value is None:
        return ""
    text = str(value).strip().casefold()
    text = unicodedata.normalize("NFKD", text)
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    text = re.sub(r"[^a-z0-9]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def normalize_identifier(value: object) -> str:
    """Keep only digits from a tax or registry identifier."""
    if value is None:
        return ""
    return re.sub(r"\D+", "", str(value))
