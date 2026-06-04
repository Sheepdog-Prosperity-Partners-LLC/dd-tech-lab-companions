# Screening a State's Medicaid Market with Public Data

Runnable notebook companion for the DD Tech Lab article:

- Article hub: <https://sheepdogprosperitypartners.com/dd-tech-lab/>
- Notebook: [`screening-a-states-medicaid-market-with-public-data.ipynb`](screening-a-states-medicaid-market-with-public-data.ipynb)

The notebook distills the verified Nevada home-care screening rig into public-safe "tech cells": NPPES provider pull, NPI-1/NPI-2 explanation, CMS Parquet/DuckDB yearly grouping, address clustering, controller rollup, growth-off-zero billing join, and OIG-LEIE timing checks.

## Public-data hygiene

The notebook ships with all outputs cleared. It does not commit provider caches, CMS Parquet files, LEIE CSV files, or generated CSV outputs. Local data files are excluded by the root `.gitignore`.

Place these files next to the notebook only when running locally:

- `cms.parquet` from the CMS provider-level Medicaid spending bulk release
- `leie.csv` from HHS-OIG LEIE, if running the exclusion join

## Run

```bash
pip install -r requirements.txt
jupyter notebook screening-a-states-medicaid-market-with-public-data.ipynb
```

The code is illustrative and uses public data only. It makes no allegation about any person or entity.
