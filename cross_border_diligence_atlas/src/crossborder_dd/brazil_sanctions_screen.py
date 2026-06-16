"""Synthetic sanctions-screening helpers for Brazil examples."""

from __future__ import annotations

from collections.abc import Iterable, Mapping

from .brazil_cnpj_parser import normalize_cnpj
from .normalize_names import normalize_name


def screen_sanctions(
    subjects: Iterable[Mapping[str, object]],
    sanctions: Iterable[Mapping[str, object]],
) -> list[dict[str, object]]:
    """Return possible sanction leads from exact identifier or normalized-name matches."""
    sanction_rows = list(sanctions)
    leads: list[dict[str, object]] = []

    for subject in subjects:
        subject_id = normalize_cnpj(subject.get("cnpj") or subject.get("identifier"))
        subject_name = normalize_name(subject.get("name") or subject.get("entity_name"))

        for sanction in sanction_rows:
            sanction_id = normalize_cnpj(sanction.get("cnpj") or sanction.get("identifier"))
            sanction_name = normalize_name(sanction.get("name") or sanction.get("entity_name"))

            match_type = ""
            if subject_id and sanction_id and subject_id == sanction_id:
                match_type = "exact_identifier"
            elif subject_name and sanction_name and subject_name == sanction_name:
                match_type = "exact_normalized_name"

            if match_type:
                leads.append(
                    {
                        "country": "Brazil",
                        "subject": subject.get("name") or subject.get("entity_name"),
                        "match_type": match_type,
                        "lead_flag": sanction.get("sanction_type", "possible_sanction_record"),
                        "limitation": "Lead only. Read the official source and escalate before treating as a finding.",
                    }
                )
    return leads
