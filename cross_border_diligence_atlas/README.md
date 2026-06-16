# Cross-Border Diligence Atlas Lab

Prepared by Noah Green CPA CFE

Public-data companion lab for the SPP Cross-Border Open-Source Diligence Atlas.

This lab teaches reproducible source-literacy methods for Brazil and Argentina from the viewpoint of a U.S. buyer, investor, lender, or diligence practitioner. It does not make legal findings, jurisdiction-level scores, suitability recommendations, or transaction advice.

## Guardrails

- Public or synthetic data only.
- No SPP client, target, or private matter data.
- Outputs are leads, not findings.
- No automated foreign-law conclusions.
- No jurisdiction-level scoring.
- No "no-hit" conclusion unless source coverage and identifier quality support it.
- Local counsel escalation is required for legal interpretation.
- Every real dataset must have source URL, access date, terms or license note, and update method in `docs/data_sources.md` or the country source docs.

## Layout

```text
src/crossborder_dd/         reusable standard-library helpers
notebooks/                  per-topic reproducible walkthroughs
data/sample/                reserved for tiny public-shape or synthetic samples
data/synthetic/             synthetic data for demonstrations
data/redacted_outputs/      publishable synthetic/redacted outputs
docs/                       source maps, limits, data dictionary, dependency review
tests/                      offline tests
```

## Article-Facing Pairs

| Example | Script | Notebook | What it demonstrates | Output |
|---|---|---|---|---|
| Brazil entity registry screen | `notebooks/BR_01_entity_registry_screen.py` | `notebooks/BR_01_entity_registry_screen.ipynb` | CNPJ normalization and source-routing context for Brazilian entity-registry follow-up. | `data/redacted_outputs/BR_01_entity_registry_screen.csv` |
| Brazil sanctions and procurement crosscheck | `notebooks/BR_02_sanctions_procurement_crosscheck.py` | `notebooks/BR_02_sanctions_procurement_crosscheck.ipynb` | Synthetic sanctions/procurement-style lead generation from exact identifier matching. | `data/redacted_outputs/BR_02_sanctions_procurement_crosscheck.csv` |
| Argentina RNS entity screen | `notebooks/AR_01_rns_entity_screen.py` | `notebooks/AR_01_rns_entity_screen.ipynb` | CUIT/CDI normalization and RNS-shaped entity-screen source literacy. | `data/redacted_outputs/AR_01_rns_entity_screen.csv` |
| Argentina boletin timeline builder | `notebooks/AR_02_boletin_timeline_builder.py` | `notebooks/AR_02_boletin_timeline_builder.ipynb` | Official-gazette-style event sorting into a diligence timeline. | `data/redacted_outputs/AR_02_boletin_timeline_builder.csv` |
| U.S. memo country-risk flags | `notebooks/US_memo_country_risk_flags.py` | `notebooks/US_memo_country_risk_flags.ipynb` | Translation of public-source leads into U.S. diligence memo flags, questions, and escalation lanes. | `data/redacted_outputs/US_memo_country_risk_flags.csv` |

## Quick Start

The helper modules use only Python standard-library modules. Install the package in editable mode or run commands with `PYTHONPATH=src`.

```bash
python3 -m pip install -e .
python3 -m pytest tests
```

If `pytest` is unavailable, the modules can still be checked with standard-library tools:

```bash
PYTHONPATH=src python3 -m compileall -q src tests
```

The tests reproduce notebook outputs without opening Jupyter by calling the same helper modules used in the notebooks.

## Dependency Posture

No third-party runtime dependency is required. See `docs/dependency_review.md` for the standard-library decision and the rejected optional charting/data-frame dependencies.

## Current Status

This repo is a tested public companion lab for synthetic Brazil and Argentina source-literacy exercises. Before adapting it to live public data:

1. Confirm source terms, API behavior, schemas, and update cadence.
2. Record source URL, access date, terms or license note, and update method in `docs/data_sources.md`.
3. Keep public notebook outputs synthetic or redacted.
4. Treat outputs as leads, not findings.
5. Escalate legal interpretation to local or specialist counsel.
