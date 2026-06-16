# Data Dictionary

Prepared by Noah Green CPA CFE

**Status:** Current for the Brazil and Argentina lab notebooks
**Last reviewed:** 2026-06-16

The committed CSV files are synthetic. Field names are intentionally plain so the notebooks can teach source literacy without implying that the samples are live government records.

## Shared Fields

| Field | Meaning | Used in | Notes |
|---|---|---|---|
| country | Country associated with the source or sample row. | All outputs | Use plain country names. Do not use this as a score or conclusion. |
| identifier | Normalized entity identifier. | BR_01, AR_01 | Digits only after normalization. |
| identifier_type | Identifier family, such as CNPJ or CUIT/CDI. | BR_01, AR_01 | Identifier type does not prove legal status. |
| identifier_valid | Format or check-digit result. | BR_01, AR_01 | A valid format is not a registry finding. |
| entity_name | Entity name as displayed in the synthetic input. | BR_01, AR_01, AR_02 | Preserve original display text for review. |
| entity_name_normalized | Conservative normalized entity name. | BR_01, AR_01 | Used for triage matching only. |
| source_surface | Public-source surface that would be checked in real diligence. | US_memo | Describes where the lead should be verified. |
| source_to_verify | Specific source or source class to check next. | US_memo | Keeps the memo tied to a source, not a conclusion. |
| owner_question | Diligence question for seller, target, or deal team. | US_memo | Should be phrased as a request for support. |
| escalation_lane | Counsel or specialist lane to involve. | US_memo | Use when a source could affect transaction terms. |
| limitation | Reason the row cannot be overread. | All outputs | Required in publishable outputs. |

## Brazil Fields

| Field | Meaning | Notes |
|---|---|---|
| cnpj | Raw Brazilian entity identifier in the synthetic input. | Formatted or unformatted inputs normalize to digits. |
| name | Synthetic entity display name. | Not sourced from a live registry. |
| match_type | How a possible sanctions/debarment lead matched. | `exact_identifier` or `exact_normalized_name` in current helper logic. |
| lead_flag | Public-source lead category. | A lead is not a finding. |
| sanction_type | Synthetic sanction/debarment category in the sample sanctions file. | Used only to demonstrate lead labeling. |

## Argentina Fields

| Field | Meaning | Notes |
|---|---|---|
| cuit | Raw Argentine entity identifier in the synthetic input. | The helper normalizes CUIT/CDI-style identifiers. |
| razon_social | Synthetic legal-name field. | Not sourced from a live registry. |
| event_date | ISO date for a synthetic official-gazette-style event. | Used for timeline sorting. |
| event_type | Synthetic notice category. | Does not classify legal effect. |
| description | Synthetic event description. | Verify real notice text before relying on any event. |
| source_url | URL field for source preservation. | Synthetic rows use `example.invalid`. |

## Publishing Rule

Do not publish client names, target names, private identifiers, or personal identifiers in notebook output. Public outputs should be synthetic or redacted and should keep the limitation field visible.
