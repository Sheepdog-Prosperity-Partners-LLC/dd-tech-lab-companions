#!/usr/bin/env python3
"""Run the Brazil CNPJ entity-registry synthetic example."""

from __future__ import annotations

import csv
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from crossborder_dd.brazil_cnpj_parser import parse_cnpj_row  # noqa: E402
from crossborder_dd.country_registry_map import sources_by_country  # noqa: E402
from crossborder_dd.export_csv import write_rows  # noqa: E402


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def build_rows(rows: list[dict[str, str]]) -> list[dict[str, object]]:
    registry_source = next(
        source
        for source in sources_by_country("Brazil")
        if "CNPJ" in source.identifiers and "parsing" in source.lab_use
    )
    redacted_rows: list[dict[str, object]] = []
    for index, row in enumerate(rows, start=1):
        parsed = parse_cnpj_row(row)
        identifier_quality = "valid_check_digit" if parsed["identifier_valid"] else "invalid_check_digit"
        lead = (
            "CNPJ format passes the check-digit test; verify against the official source before relying."
            if parsed["identifier_valid"]
            else "CNPJ format fails the check-digit test; correct intake data before registry follow-up."
        )
        redacted_rows.append(
            {
                "country": parsed["country"],
                "synthetic_subject_id": f"SYN-BR-{index:03d}",
                "entity_label": f"SYNTHETIC_BR_ENTITY_{index:03d}",
                "identifier_type": parsed["identifier_type"],
                "identifier_last4": parsed["identifier"][-4:],
                "identifier_quality": identifier_quality,
                "official_source_for_next_step": registry_source.source_name,
                "source_access_method": registry_source.access_method,
                "source_literacy_lead": lead,
                "required_escalation": (
                    "Escalate to Brazil local counsel before treating registry status, legal form, "
                    "authority, or legal effect as established."
                ),
                "publication_limitation": (
                    "Synthetic lead only; no registry query, entity-status finding, legal conclusion, "
                    "jurisdiction-level score, or no-hit inference."
                ),
            }
        )
    return redacted_rows


def main() -> None:
    data_path = ROOT / "data" / "synthetic" / "brazil_entities.csv"
    output_path = ROOT / "data" / "redacted_outputs" / "BR_01_entity_registry_screen.csv"
    rows = build_rows(read_rows(data_path))
    write_rows(output_path, rows)
    print(f"Wrote {len(rows)} synthetic rows to {output_path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
