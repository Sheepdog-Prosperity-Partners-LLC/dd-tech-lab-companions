#!/usr/bin/env python3
"""Run the Brazil sanctions and procurement synthetic crosscheck."""

from __future__ import annotations

import csv
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from crossborder_dd.brazil_sanctions_screen import screen_sanctions  # noqa: E402
from crossborder_dd.export_csv import write_rows  # noqa: E402


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def build_rows(subjects: list[dict[str, str]], sanctions: list[dict[str, str]]) -> list[dict[str, object]]:
    return [
        {
            "country": lead["country"],
            "subject": lead["subject"],
            "match_type": lead["match_type"],
            "lead_flag": lead["lead_flag"],
            "source_shape": "synthetic Brazil sanctions/procurement crosscheck",
            "sanctions_escalation": (
                "Confirm against the official sanctions or debarment source before relying on the lead."
            ),
            "procurement_escalation": (
                "Check applicable procurement eligibility, debarment, contract, and source-update rules."
            ),
            "local_counsel_escalation": (
                "Escalate to qualified Brazil local counsel before legal interpretation or transaction advice."
            ),
            "limitation": lead["limitation"],
            "output_status": "lead_only_no_legal_conclusion",
        }
        for lead in screen_sanctions(subjects, sanctions)
    ]


def main() -> None:
    subjects = read_rows(ROOT / "data" / "synthetic" / "brazil_entities.csv")
    sanctions = read_rows(ROOT / "data" / "synthetic" / "brazil_sanctions.csv")
    output_path = ROOT / "data" / "redacted_outputs" / "BR_02_sanctions_procurement_crosscheck.csv"
    rows = build_rows(subjects, sanctions)
    write_rows(output_path, rows)
    print(f"Wrote {len(rows)} synthetic leads to {output_path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
