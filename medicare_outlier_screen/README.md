# Medicare Outlier Screen

Prepared by Noah Green CPA CFE.

Runnable script and notebook companion for the Medicare outlier screen in the False Claims Act data-relator series.

The screen uses public CMS Medicare provider-service data when run live. The paired notebook uses a tiny synthetic CMS-shaped cache so the repo can execute without network access and without naming real providers.

## Files

| Artifact | Purpose |
|---|---|
| `medicare_outlier_screen.py` | Runnable peer-relative outlier screen |
| `medicare_outlier_screen.ipynb` | Notebook form of the same screen |
| `data/sample/medicare_hcpcs_36902_synthetic.csv` | Synthetic CMS-shaped fixture |

## Run

```bash
pip install -r requirements.txt
python medicare_outlier_screen.py --hcpcs 36902 --cache data/sample/medicare_hcpcs_36902_synthetic.csv --min-peers 5 --z 2.0 --out /tmp/medicare_outlier_synthetic.csv
```

The output is a triage lead list, not a finding. A high peer-relative intensity score is a question for records-level review, not proof of fraud.
