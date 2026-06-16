# National-Security Diligence Lab

Prepared by Noah Green CPA CFE.

This folder is the reparented Applied DD Lab companion for the SPP National-Security Diligence Stack. It now lives as a child folder of the canonical DD Tech Lab companion repository:

<https://github.com/Sheepdog-Prosperity-Partners-LLC/dd-tech-lab-companions/tree/main/national_security_diligence>

The former standalone repository is preserved as an archived redirect for older public links.

## Guardrails

- Public, synthetic, redacted, or publication-approved public case data only.
- No SPP client, target, or private matter data.
- Outputs are leads, not findings.
- A list hit is a lead, not a finding. Check the official list and restrictions before relying on it.
- BOI is never treated as a public bulk dataset.
- Export classification is not automated.
- Every real dataset has a source URL, access date, terms or license note, and update method in `docs/data_sources.md`.

## Layout

```text
src/ns_diligence/          reusable package helpers
notebooks/                 article-facing wrapper scripts and paired notebooks
data/sample/               small publication-approved public-shape samples
data/synthetic/            synthetic data for demonstrations
data/redacted_outputs/     publishable sample outputs
docs/                      data sources, limitations, dependency review, update log
tests/                     offline tests plus optional live-source shape tests
```

## Article-Facing Pairs

| Article | Script | Notebook |
|---|---|---|
| A1 CFIUS public actions | `notebooks/A1_cfius_public_actions.py` | `notebooks/A1_cfius_public_actions.ipynb` |
| A2 outbound triage | `notebooks/A2_outbound_triage.py` | `notebooks/A2_outbound_triage.ipynb` |
| C1 data threshold checker | `notebooks/C1_data_threshold_checker.py` | `notebooks/C1_data_threshold_checker.ipynb` |
| C2 forfeiture timeline builder | `notebooks/C2_forfeiture_timeline_builder.py` | `notebooks/C2_forfeiture_timeline_builder.ipynb` |
| C3 bounty program matrix | `notebooks/C3_bounty_program_matrix.py` | `notebooks/C3_bounty_program_matrix.ipynb` |
| D1 integrated workflow | `notebooks/D1_integrated_workflow.py` | `notebooks/D1_integrated_workflow.ipynb` |
| D2 screening toolkit | `notebooks/D2_screening_toolkit.py` | `notebooks/D2_screening_toolkit.ipynb` |
| D3 remedy comparison timeline | `notebooks/D3_remedy_comparison_timeline.py` | `notebooks/D3_remedy_comparison_timeline.ipynb` |

## Quick Start

Run from this folder:

```bash
PYTHONPATH=src python3 -m unittest discover -s tests -p 'test_*.py'
```

```bash
PYTHONPATH=src python3 -m compileall -q src tests ns_screen.py notebooks
```

Run an article-facing wrapper:

```bash
PYTHONPATH=src python3 notebooks/A2_outbound_triage.py
```

Run a paired notebook:

```bash
jupyter nbconvert --execute --to notebook --inplace notebooks/A2_outbound_triage.ipynb
```

## Live Sources

The optional live-source commands reach official public endpoints for source-shape checks only. They do not certify legal currency, list completeness, or any particular match.

```bash
NS_DILIGENCE_LIVE=1 PYTHONPATH=src python3 -m unittest tests/test_live_sources.py
```

## Current Status

The child folder includes the A1, A2, C1, C2, C3, D1, D2, and D3 article-facing pairs, reusable package modules, tests, source documentation, and redacted or synthetic sample outputs.
