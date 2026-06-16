"""Brazil CNPJ parsing helpers for synthetic or public-source rows."""

from __future__ import annotations

from collections.abc import Mapping

from .normalize_names import normalize_identifier, normalize_name


def normalize_cnpj(value: object) -> str:
    return normalize_identifier(value)


def is_valid_cnpj(value: object) -> bool:
    """Validate a CNPJ check digit.

    This is an identifier-quality check. It does not prove the entity exists.
    """
    digits = normalize_cnpj(value)
    if len(digits) != 14 or len(set(digits)) == 1:
        return False

    def check_digit(base: str, weights: tuple[int, ...]) -> str:
        total = sum(int(digit) * weight for digit, weight in zip(base, weights))
        remainder = total % 11
        return "0" if remainder < 2 else str(11 - remainder)

    first = check_digit(digits[:12], (5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2))
    second = check_digit(digits[:12] + first, (6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2))
    return digits[-2:] == first + second


def parse_cnpj_row(row: Mapping[str, object]) -> dict[str, object]:
    raw_id = row.get("cnpj") or row.get("CNPJ") or row.get("identifier")
    raw_name = row.get("name") or row.get("razao_social") or row.get("entity_name")
    cnpj = normalize_cnpj(raw_id)
    return {
        "country": "Brazil",
        "identifier": cnpj,
        "identifier_type": "CNPJ",
        "identifier_valid": is_valid_cnpj(cnpj),
        "entity_name": "" if raw_name is None else str(raw_name).strip(),
        "entity_name_normalized": normalize_name(raw_name),
    }
