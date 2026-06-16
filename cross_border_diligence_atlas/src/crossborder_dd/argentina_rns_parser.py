"""Argentina RNS parsing helpers for synthetic or public-source rows."""

from __future__ import annotations

from collections.abc import Mapping

from .normalize_names import normalize_identifier, normalize_name


def normalize_cuit(value: object) -> str:
    return normalize_identifier(value)


def is_valid_cuit(value: object) -> bool:
    """Validate CUIT/CUIL-style check digit.

    This checks identifier format only. It does not prove registry status.
    """
    digits = normalize_cuit(value)
    if len(digits) != 11 or len(set(digits)) == 1:
        return False
    weights = (5, 4, 3, 2, 7, 6, 5, 4, 3, 2)
    total = sum(int(digit) * weight for digit, weight in zip(digits[:10], weights))
    check = 11 - (total % 11)
    if check == 11:
        check = 0
    elif check == 10:
        check = 9
    return int(digits[-1]) == check


def parse_rns_row(row: Mapping[str, object]) -> dict[str, object]:
    raw_id = row.get("cuit") or row.get("CUIT") or row.get("identifier")
    raw_name = row.get("razon_social") or row.get("name") or row.get("entity_name")
    cuit = normalize_cuit(raw_id)
    return {
        "country": "Argentina",
        "identifier": cuit,
        "identifier_type": "CUIT/CDI",
        "identifier_valid": is_valid_cuit(cuit),
        "entity_name": "" if raw_name is None else str(raw_name).strip(),
        "entity_name_normalized": normalize_name(raw_name),
    }
