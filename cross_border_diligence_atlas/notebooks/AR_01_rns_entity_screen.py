#!/usr/bin/env python3
"""Run the Argentina RNS synthetic entity-screen example."""

from __future__ import annotations

import csv
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from crossborder_dd.argentina_rns_parser import parse_rns_row  # noqa: E402


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def mask_identifier(identifier: object) -> str:
    digits = str(identifier or "")
    if len(digits) <= 4:
        return "REDACTED"
    return f"{digits[:2]}*******{digits[-2:]}"


def lead_flag(parsed_row: dict[str, object]) -> str:
    if parsed_row["identifier_valid"]:
        return "format_passes_check_digit"
    return "format_fails_check_digit"


def build_rows(rows: list[dict[str, str]]) -> list[dict[str, object]]:
    redacted_rows: list[dict[str, object]] = []
    for index, row in enumerate(rows, start=1):
        parsed = parse_rns_row(row)
        redacted_rows.append(
            {
                "sample_id": f"AR_RNS_SYN_{index:02d}",
                "country": parsed["country"],
                "source_name": "Registro Nacional de Sociedades synthetic fixture",
                "identifier_type": parsed["identifier_type"],
                "identifier_redacted": mask_identifier(parsed["identifier"]),
                "entity_name_redacted": f"SYNTHETIC_ENTITY_{index:02d}",
                "entity_name_normalized": parsed["entity_name_normalized"],
                "identifier_valid": parsed["identifier_valid"],
                "match_type": "identifier_format_check",
                "lead_flag": lead_flag(parsed),
                "limitation": (
                    "Synthetic row only; a format result or no-hit does not prove registration, "
                    "good standing, ownership, authority, or adverse status."
                ),
                "escalation_note": (
                    "Escalate to Argentina local counsel before interpreting legal status or using this result in deal terms."
                ),
            }
        )
    return redacted_rows


def write_rows(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    data_path = ROOT / "data" / "synthetic" / "argentina_rns.csv"
    output_path = ROOT / "data" / "redacted_outputs" / "AR_01_rns_entity_screen.csv"
    rows = build_rows(read_rows(data_path))
    write_rows(output_path, rows)
    print(f"Wrote {len(rows)} synthetic rows to {output_path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
