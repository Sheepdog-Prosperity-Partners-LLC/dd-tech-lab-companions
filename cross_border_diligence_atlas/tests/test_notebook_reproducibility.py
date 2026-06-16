import csv
from pathlib import Path

from crossborder_dd.argentina_rns_parser import parse_rns_row
from crossborder_dd.brazil_cnpj_parser import parse_cnpj_row
from crossborder_dd.brazil_sanctions_screen import screen_sanctions
from crossborder_dd.country_registry_map import sources_by_country
from crossborder_dd.gazette_timeline_builder import build_timeline


ROOT = Path(__file__).resolve().parents[1]
SYNTHETIC = ROOT / "data" / "synthetic"
OUTPUTS = ROOT / "data" / "redacted_outputs"


def read_csv(path):
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def stringify(rows):
    return [{key: str(value) for key, value in row.items()} for row in rows]


def mask_identifier(identifier):
    digits = str(identifier or "")
    if len(digits) <= 4:
        return "REDACTED"
    return f"{digits[:2]}*******{digits[-2:]}"


def expected_br_01_rows():
    registry_source = next(
        source
        for source in sources_by_country("Brazil")
        if "CNPJ" in source.identifiers and "parsing" in source.lab_use
    )
    rows = []
    for index, row in enumerate(read_csv(SYNTHETIC / "brazil_entities.csv"), start=1):
        parsed = parse_cnpj_row(row)
        quality = "valid_check_digit" if parsed["identifier_valid"] else "invalid_check_digit"
        lead = (
            "CNPJ format passes the check-digit test; verify against the official source before relying."
            if parsed["identifier_valid"]
            else "CNPJ format fails the check-digit test; correct intake data before registry follow-up."
        )
        rows.append(
            {
                "country": "Brazil",
                "synthetic_subject_id": f"SYN-BR-{index:03d}",
                "entity_label": f"SYNTHETIC_BR_ENTITY_{index:03d}",
                "identifier_type": parsed["identifier_type"],
                "identifier_last4": parsed["identifier"][-4:],
                "identifier_quality": quality,
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
    return stringify(rows)


def expected_br_02_rows():
    subjects = read_csv(SYNTHETIC / "brazil_entities.csv")
    sanctions = read_csv(SYNTHETIC / "brazil_sanctions.csv")
    rows = []
    for lead in screen_sanctions(subjects, sanctions):
        rows.append(
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
        )
    return stringify(rows)


def expected_ar_01_rows():
    rows = []
    for index, row in enumerate(read_csv(SYNTHETIC / "argentina_rns.csv"), start=1):
        parsed = parse_rns_row(row)
        rows.append(
            {
                "sample_id": f"AR_RNS_SYN_{index:02d}",
                "country": "Argentina",
                "source_name": "Registro Nacional de Sociedades synthetic fixture",
                "identifier_type": parsed["identifier_type"],
                "identifier_redacted": mask_identifier(parsed["identifier"]),
                "entity_name_redacted": f"SYNTHETIC_ENTITY_{index:02d}",
                "entity_name_normalized": parsed["entity_name_normalized"],
                "identifier_valid": parsed["identifier_valid"],
                "match_type": "identifier_format_check",
                "lead_flag": (
                    "format_passes_check_digit"
                    if parsed["identifier_valid"]
                    else "format_fails_check_digit"
                ),
                "limitation": (
                    "Synthetic row only; a format result or no-hit does not prove registration, "
                    "good standing, ownership, authority, or adverse status."
                ),
                "escalation_note": (
                    "Escalate to Argentina local counsel before interpreting legal status or using this result in deal terms."
                ),
            }
        )
    return stringify(rows)


def expected_ar_02_rows():
    rows = read_csv(SYNTHETIC / "gazette_events.csv")
    return stringify(build_timeline(rows, "Sociedad Sintetica Argentina SA"))


def expected_us_memo_rows():
    return [
        {
            "sample_id": "SYN-US-MEMO-001",
            "source_shape": "registry_identifier_output",
            "memo_flag": "Registry identifier or extract gap",
            "synthetic_trigger": "identifier is missing, malformed, or not tied to a current official extract",
            "owner_question": "Do we have the authoritative legal name, identifier, current registry extract, and filing date from the official source?",
            "source_to_verify": "Official entity registry or equivalent corporate register",
            "escalation_lane": "Local counsel or corporate-registry specialist",
            "what_this_proves": "The memo team has a structured reason to request the official registry extract.",
            "what_it_cannot_prove": "It cannot prove existence, good standing, ownership, authority, or legal capacity.",
            "match_type": "identifier_quality",
            "source_name": "Official entity registry or equivalent corporate register",
            "limitation": "Identifier quality supports routing only. It does not prove current entity status.",
            "redaction_status": "synthetic_redacted_no_private_data",
        },
        {
            "sample_id": "SYN-US-MEMO-002",
            "source_shape": "registry_identifier_output",
            "memo_flag": "Authority, standing, or filing-status gap",
            "synthetic_trigger": "normalized identifier exists but current standing, directors, or authority fields are not verified",
            "owner_question": "Which current source proves status, authorized signers, directors, beneficial ownership hooks, and any filed changes?",
            "source_to_verify": "Current registry extract, filing history, constitutional documents, and local status certificate where available",
            "escalation_lane": "Local counsel or corporate governance specialist",
            "what_this_proves": "The memo team can separate identifier normalization from status and authority verification.",
            "what_it_cannot_prove": "It cannot prove who controls the entity or who can bind it without authoritative documents.",
            "match_type": "registry_extract_needed",
            "source_name": "Official entity registry, current extract, and filing history",
            "limitation": "A valid-looking identifier does not prove good standing, control, or authority to bind.",
            "redaction_status": "synthetic_redacted_no_private_data",
        },
        {
            "sample_id": "SYN-US-MEMO-003",
            "source_shape": "exact_match_screening_output",
            "memo_flag": "Exact-identifier public-restriction lead",
            "synthetic_trigger": "exact identifier match appears in a sanctions, debarment, procurement, or regulator-style list",
            "owner_question": "Is the exact-identifier lead current, in scope for this party, and tied to an applicable restriction, exclusion, or enforcement record?",
            "source_to_verify": "Official sanctions, procurement exclusion, enforcement, regulator, or licensing list",
            "escalation_lane": "Sanctions, export-controls, anti-corruption, or public-procurement specialist counsel",
            "what_this_proves": "The memo team has a source-specific lead that requires official-record review before reliance.",
            "what_it_cannot_prove": "It cannot prove violation, current restriction, transaction prohibition, or culpability.",
            "match_type": "exact_identifier",
            "source_name": "Official sanctions, procurement exclusion, enforcement, or regulator list",
            "limitation": "An exact identifier lead is a memo flag, not a finding. Read the official record and test scope, date, and party coverage.",
            "redaction_status": "synthetic_redacted_no_private_data",
        },
        {
            "sample_id": "SYN-US-MEMO-004",
            "source_shape": "exact_match_screening_output",
            "memo_flag": "Name-only public-record ambiguity",
            "synthetic_trigger": "normalized-name match appears without an exact identifier or sufficient disambiguating fields",
            "owner_question": "What identifier, address, officer, affiliate, date, or source field disambiguates the name-only hit?",
            "source_to_verify": "Official list record, registry record, and corroborating source fields used for disambiguation",
            "escalation_lane": "Diligence lead plus local/specialist counsel if the ambiguity could affect a memo conclusion",
            "what_this_proves": "The memo team has a possible ambiguity that should not be overread.",
            "what_it_cannot_prove": "It cannot prove the record belongs to the same party without corroborating identifiers.",
            "match_type": "exact_normalized_name",
            "source_name": "Official list plus registry records that can disambiguate name, identifier, location, and affiliates",
            "limitation": "Name-only matches are ambiguity flags. They cannot identify the party without corroborating source fields.",
            "redaction_status": "synthetic_redacted_no_private_data",
        },
        {
            "sample_id": "SYN-US-MEMO-005",
            "source_shape": "official_notice_timeline_output",
            "memo_flag": "Official-notice timeline needs legal-effect review",
            "synthetic_trigger": "official-notice events appear in sequence, but legal effect and current status are unclear",
            "owner_question": "What did each notice actually do, when did it take effect, and does a later filing modify or cure the issue?",
            "source_to_verify": "Official gazette, court docket, regulator notice, registry filing, or linked proceeding record",
            "escalation_lane": "Local counsel or litigation, insolvency, regulatory, or corporate specialist",
            "what_this_proves": "The memo team can build a chronological source trail for counsel and deal owners.",
            "what_it_cannot_prove": "It cannot interpret legal effect, current status, or materiality without source review and counsel input.",
            "match_type": "timeline_sequence",
            "source_name": "Official gazette, court docket, regulator notice, or filing bulletin",
            "limitation": "A notice timeline shows that events were published. It does not interpret their legal effect.",
            "redaction_status": "synthetic_redacted_no_private_data",
        },
        {
            "sample_id": "SYN-US-MEMO-006",
            "source_shape": "official_notice_timeline_output",
            "memo_flag": "Recent public-source event timing question",
            "synthetic_trigger": "recent notice appears near a diligence date, signing milestone, financing step, or operating-license review",
            "owner_question": "Does the recent event affect signing authority, licenses, financing conditions, closing deliverables, or post-closing covenants?",
            "source_to_verify": "Official notice text and linked registry, court, regulator, licensing, or procurement file",
            "escalation_lane": "Local counsel, specialist counsel, and deal lead for timing/materiality triage",
            "what_this_proves": "The memo team has a dated event that should be placed against the deal timeline.",
            "what_it_cannot_prove": "It cannot establish materiality, breach, violation, or transaction impact by timing alone.",
            "match_type": "event_timing",
            "source_name": "Official notice text and any linked court, regulator, licensing, or registry file",
            "limitation": "Timing proximity is a question prompt only. It does not establish materiality or transaction impact.",
            "redaction_status": "synthetic_redacted_no_private_data",
        },
    ]


def assert_output_matches(filename, expected_rows):
    actual = read_csv(OUTPUTS / filename)
    assert actual == expected_rows


def test_br_01_output_reproduces_without_notebook():
    assert_output_matches("BR_01_entity_registry_screen.csv", expected_br_01_rows())


def test_br_02_output_reproduces_without_notebook():
    assert_output_matches("BR_02_sanctions_procurement_crosscheck.csv", expected_br_02_rows())


def test_ar_01_output_reproduces_without_notebook():
    assert_output_matches("AR_01_rns_entity_screen.csv", expected_ar_01_rows())


def test_ar_02_output_reproduces_without_notebook():
    assert_output_matches("AR_02_boletin_timeline_builder.csv", expected_ar_02_rows())


def test_us_memo_output_reproduces_without_notebook():
    assert_output_matches("US_memo_country_risk_flags.csv", expected_us_memo_rows())
