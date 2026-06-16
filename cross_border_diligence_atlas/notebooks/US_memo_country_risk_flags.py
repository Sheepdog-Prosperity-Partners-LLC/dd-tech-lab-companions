#!/usr/bin/env python3
"""Build U.S.-buyer memo flags from synthetic cross-border source leads."""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

SYNTHETIC_SOURCE_LEADS = [
    {
        "sample_id": "SYN-US-MEMO-001",
        "source_shape": "registry_identifier_output",
        "lead_flag": "identifier_format_or_extract_gap",
        "synthetic_trigger": "identifier is missing, malformed, or not tied to a current official extract",
        "match_type": "identifier_quality",
        "source_name": "Official entity registry or equivalent corporate register",
        "limitation": "Identifier quality supports routing only. It does not prove current entity status.",
    },
    {
        "sample_id": "SYN-US-MEMO-002",
        "source_shape": "registry_identifier_output",
        "lead_flag": "authority_and_status_gap",
        "synthetic_trigger": (
            "normalized identifier exists but current standing, directors, or authority fields are not verified"
        ),
        "match_type": "registry_extract_needed",
        "source_name": "Official entity registry, current extract, and filing history",
        "limitation": "A valid-looking identifier does not prove good standing, control, or authority to bind.",
    },
    {
        "sample_id": "SYN-US-MEMO-003",
        "source_shape": "exact_match_screening_output",
        "lead_flag": "public_restriction_exact_identifier",
        "synthetic_trigger": (
            "exact identifier match appears in a sanctions, debarment, procurement, or regulator-style list"
        ),
        "match_type": "exact_identifier",
        "source_name": "Official sanctions, procurement exclusion, enforcement, or regulator list",
        "limitation": (
            "An exact identifier lead is a memo flag, not a finding. Read the official record and test scope, "
            "date, and party coverage."
        ),
    },
    {
        "sample_id": "SYN-US-MEMO-004",
        "source_shape": "exact_match_screening_output",
        "lead_flag": "name_only_ambiguity",
        "synthetic_trigger": "normalized-name match appears without an exact identifier or sufficient disambiguating fields",
        "match_type": "exact_normalized_name",
        "source_name": "Official list plus registry records that can disambiguate name, identifier, location, and affiliates",
        "limitation": "Name-only matches are ambiguity flags. They cannot identify the party without corroborating source fields.",
    },
    {
        "sample_id": "SYN-US-MEMO-005",
        "source_shape": "official_notice_timeline_output",
        "lead_flag": "timeline_legal_effect_unknown",
        "synthetic_trigger": "official-notice events appear in sequence, but legal effect and current status are unclear",
        "match_type": "timeline_sequence",
        "source_name": "Official gazette, court docket, regulator notice, or filing bulletin",
        "limitation": "A notice timeline shows that events were published. It does not interpret their legal effect.",
    },
    {
        "sample_id": "SYN-US-MEMO-006",
        "source_shape": "official_notice_timeline_output",
        "lead_flag": "recent_event_timing_gap",
        "synthetic_trigger": (
            "recent notice appears near a diligence date, signing milestone, financing step, or operating-license review"
        ),
        "match_type": "event_timing",
        "source_name": "Official notice text and any linked court, regulator, licensing, or registry file",
        "limitation": (
            "Timing proximity is a question prompt only. It does not establish materiality or transaction impact."
        ),
    },
]

FLAG_TEMPLATES = {
    "identifier_format_or_extract_gap": {
        "memo_flag": "Registry identifier or extract gap",
        "owner_question": (
            "Do we have the authoritative legal name, identifier, current registry extract, "
            "and filing date from the official source?"
        ),
        "source_to_verify": "Official entity registry or equivalent corporate register",
        "escalation_lane": "Local counsel or corporate-registry specialist",
        "what_this_proves": "The memo team has a structured reason to request the official registry extract.",
        "what_it_cannot_prove": "It cannot prove existence, good standing, ownership, authority, or legal capacity.",
    },
    "authority_and_status_gap": {
        "memo_flag": "Authority, standing, or filing-status gap",
        "owner_question": (
            "Which current source proves status, authorized signers, directors, beneficial ownership hooks, "
            "and any filed changes?"
        ),
        "source_to_verify": (
            "Current registry extract, filing history, constitutional documents, and local status certificate where available"
        ),
        "escalation_lane": "Local counsel or corporate governance specialist",
        "what_this_proves": "The memo team can separate identifier normalization from status and authority verification.",
        "what_it_cannot_prove": "It cannot prove who controls the entity or who can bind it without authoritative documents.",
    },
    "public_restriction_exact_identifier": {
        "memo_flag": "Exact-identifier public-restriction lead",
        "owner_question": (
            "Is the exact-identifier lead current, in scope for this party, and tied to an applicable restriction, "
            "exclusion, or enforcement record?"
        ),
        "source_to_verify": "Official sanctions, procurement exclusion, enforcement, regulator, or licensing list",
        "escalation_lane": "Sanctions, export-controls, anti-corruption, or public-procurement specialist counsel",
        "what_this_proves": "The memo team has a source-specific lead that requires official-record review before reliance.",
        "what_it_cannot_prove": "It cannot prove violation, current restriction, transaction prohibition, or culpability.",
    },
    "name_only_ambiguity": {
        "memo_flag": "Name-only public-record ambiguity",
        "owner_question": "What identifier, address, officer, affiliate, date, or source field disambiguates the name-only hit?",
        "source_to_verify": "Official list record, registry record, and corroborating source fields used for disambiguation",
        "escalation_lane": "Diligence lead plus local/specialist counsel if the ambiguity could affect a memo conclusion",
        "what_this_proves": "The memo team has a possible ambiguity that should not be overread.",
        "what_it_cannot_prove": "It cannot prove the record belongs to the same party without corroborating identifiers.",
    },
    "timeline_legal_effect_unknown": {
        "memo_flag": "Official-notice timeline needs legal-effect review",
        "owner_question": "What did each notice actually do, when did it take effect, and does a later filing modify or cure the issue?",
        "source_to_verify": "Official gazette, court docket, regulator notice, registry filing, or linked proceeding record",
        "escalation_lane": "Local counsel or litigation, insolvency, regulatory, or corporate specialist",
        "what_this_proves": "The memo team can build a chronological source trail for counsel and deal owners.",
        "what_it_cannot_prove": "It cannot interpret legal effect, current status, or materiality without source review and counsel input.",
    },
    "recent_event_timing_gap": {
        "memo_flag": "Recent public-source event timing question",
        "owner_question": (
            "Does the recent event affect signing authority, licenses, financing conditions, closing deliverables, "
            "or post-closing covenants?"
        ),
        "source_to_verify": "Official notice text and linked registry, court, regulator, licensing, or procurement file",
        "escalation_lane": "Local counsel, specialist counsel, and deal lead for timing/materiality triage",
        "what_this_proves": "The memo team has a dated event that should be placed against the deal timeline.",
        "what_it_cannot_prove": (
            "It cannot establish materiality, breach, violation, or transaction impact by timing alone."
        ),
    },
}

FIELDNAMES = [
    "sample_id",
    "source_shape",
    "memo_flag",
    "synthetic_trigger",
    "owner_question",
    "source_to_verify",
    "escalation_lane",
    "what_this_proves",
    "what_it_cannot_prove",
    "match_type",
    "source_name",
    "limitation",
    "redaction_status",
]


def build_memo_flags() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for lead in SYNTHETIC_SOURCE_LEADS:
        template = FLAG_TEMPLATES[lead["lead_flag"]]
        rows.append(
            {
                "sample_id": lead["sample_id"],
                "source_shape": lead["source_shape"],
                "memo_flag": template["memo_flag"],
                "synthetic_trigger": lead["synthetic_trigger"],
                "owner_question": template["owner_question"],
                "source_to_verify": template["source_to_verify"],
                "escalation_lane": template["escalation_lane"],
                "what_this_proves": template["what_this_proves"],
                "what_it_cannot_prove": template["what_it_cannot_prove"],
                "match_type": lead["match_type"],
                "source_name": lead["source_name"],
                "limitation": lead["limitation"],
                "redaction_status": "synthetic_redacted_no_private_data",
            }
        )
    return rows


def main() -> None:
    output_path = ROOT / "data" / "redacted_outputs" / "US_memo_country_risk_flags.csv"
    rows = build_memo_flags()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {len(rows)} synthetic memo flags to {output_path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
