"""Build simple timelines from public-gazette-style event rows."""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from datetime import date

from .normalize_names import normalize_name


def parse_iso_date(value: object) -> date:
    if isinstance(value, date):
        return value
    return date.fromisoformat(str(value))


def build_timeline(rows: Iterable[Mapping[str, object]], entity_name: str | None = None) -> list[dict[str, object]]:
    wanted = normalize_name(entity_name) if entity_name else ""
    events: list[dict[str, object]] = []
    for row in rows:
        row_name = normalize_name(row.get("entity_name") or row.get("name"))
        if wanted and row_name != wanted:
            continue
        events.append(
            {
                "event_date": parse_iso_date(row.get("event_date")).isoformat(),
                "entity_name": row.get("entity_name") or row.get("name"),
                "event_type": row.get("event_type", "notice"),
                "description": row.get("description", ""),
                "source_url": row.get("source_url", ""),
                "limitation": "Timeline lead only. Verify notice text in the official source.",
            }
        )
    return sorted(events, key=lambda event: event["event_date"])
