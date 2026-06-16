# Contributing

Prepared by Noah Green CPA CFE.

This repository is the canonical DD Tech Lab companion-code home for Sheepdog Prosperity Partners.

## Duality Rule

Every worked computational companion must ship in two forms:

| Form | Purpose |
|---|---|
| `.py` | Direct runnable script for terminal execution and CI checks |
| `.ipynb` | Narrated notebook for readers who want to reproduce the method step by step |

For simple companion folders, the script and notebook must have the same stem. Example:

```text
stochastic_markov/008_two_stage_screen.py
stochastic_markov/008_two_stage_screen.ipynb
```

For module-backed vertical labs, reusable package code may live under `src/`, while article-facing wrappers live next to the notebooks. Example:

```text
national_security_diligence/notebooks/A1_cfius_public_actions.py
national_security_diligence/notebooks/A1_cfius_public_actions.ipynb
```

The CI workflow runs `tools/check_duality.py` and fails if a tracked companion root has a script without its paired notebook, or a notebook without its paired script.

## Public-Data Hygiene

Do not commit large public-data caches, DuckDB databases, Parquet files, generated provider pulls, or private matter data. Keep examples synthetic, redacted, or publication-approved public data.

Small sample CSV files under `data/sample/`, `data/synthetic/`, and `data/redacted_outputs/` are allowed when they are necessary for a notebook to run offline.

## Output Claims

Do not hand-enter figures into notebooks. Every printed number must come from running the paired code. If the code output diverges from the article text, log the divergence and hold the article or companion for review.
