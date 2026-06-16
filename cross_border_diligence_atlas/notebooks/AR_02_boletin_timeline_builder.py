#!/usr/bin/env python3
"""Run the Argentina official-notice timeline synthetic example."""

from __future__ import annotations

import csv
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from crossborder_dd.export_csv import write_rows  # noqa: E402
from crossborder_dd.gazette_timeline_builder import build_timeline  # noqa: E402


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def main() -> None:
    data_path = ROOT / "data" / "synthetic" / "gazette_events.csv"
    output_path = ROOT / "data" / "redacted_outputs" / "AR_02_boletin_timeline_builder.csv"
    timeline = build_timeline(read_rows(data_path), "Sociedad Sintetica Argentina SA")
    assert [event["event_date"] for event in timeline] == sorted(event["event_date"] for event in timeline)
    assert all(event["limitation"] for event in timeline)
    write_rows(output_path, timeline)
    print(f"Wrote {len(timeline)} synthetic events to {output_path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
