# DD Tech Lab Companions

[![DOI](https://zenodo.org/badge/1239117464.svg)](https://zenodo.org/badge/latestdoi/1239117464)

Prepared by Noah Green CPA CFE.

> Citation: each tagged release of this repository is archived on Zenodo and assigned a DOI. The badge above resolves to the latest version DOI once the first GitHub release is published. See `CITATION.cff` for citation metadata.

Runnable Python and notebook companions for DD Tech Lab articles published by Sheepdog Prosperity Partners.

Canonical repository: <https://github.com/Sheepdog-Prosperity-Partners-LLC/dd-tech-lab-companions>

Each worked computational companion ships with both a runnable `.py` script and a paired `.ipynb` notebook. Scripts are for direct execution and CI checks. Notebooks are the reader-facing walkthroughs.

## Companion Map

| Article | Folder | Python | Notebook |
|---|---|---|---|
| [First-Order Markov Modeling for Transaction-Stream Analysis in Audit](https://sheepdogprosperitypartners.com/why-markov-chains-belong-in-financial-statement-audit/) | `stochastic_markov/` | `001_markov_intro.py` | `001_markov_intro.ipynb` |
| [Modeling Journal-Entry Sequences in Production](https://sheepdogprosperitypartners.com/modeling-journal-entry-sequences-in-production/) | `stochastic_markov/` | `002_journal_entry_production.py` | `002_journal_entry_production.ipynb` |
| [Hidden Markov Models for Earnings-Management Regime Detection](https://sheepdogprosperitypartners.com/hidden-markov-models-earnings-management-regime-detection/) | `stochastic_markov/` | `003_hidden_markov_earnings_management.py` | `003_hidden_markov_earnings_management.ipynb` |
| [Markov Mixture Models for Round-Tripping and Lapping Detection](https://sheepdogprosperitypartners.com/markov-mixture-models-round-tripping-lapping/) | `stochastic_markov/` | `004_mixture_round_tripping.py` | `004_mixture_round_tripping.ipynb` |
| [Random-Walk and Stationarity Tests on Account Reconciliations](https://sheepdogprosperitypartners.com/random-walk-stationarity-tests-account-reconciliations/) | `stochastic_markov/` | `005_random_walk_stationarity.py` | `005_random_walk_stationarity.ipynb` |
| [Markov Decision Processes for Risk-Based Audit Sampling](https://sheepdogprosperitypartners.com/markov-decision-processes-risk-based-audit-sampling/) | `stochastic_markov/` | `006_markov_decision_audit_sampling.py` | `006_markov_decision_audit_sampling.ipynb` |
| [Stochastic Volatility Models for Restatement-Timing Anomalies](https://sheepdogprosperitypartners.com/stochastic-volatility-restatement-timing/) | `stochastic_markov/` | `007_garch_restatement_timing.py` | `007_garch_restatement_timing.ipynb` |
| [Two-Stage Screening: Benford's Law plus First-Order Markov](https://sheepdogprosperitypartners.com/two-stage-screening-benford-first-order-markov/) | `stochastic_markov/` | `008_two_stage_screen.py` | `008_two_stage_screen.ipynb` |
| [Higher-Order and Variable-Order Markov Models for Long-Memory Fraud Schemes](https://sheepdogprosperitypartners.com/higher-order-variable-order-markov-long-memory/) | `stochastic_markov/` | `009_higher_order_variable_order_markov.py` | `009_higher_order_variable_order_markov.ipynb` |
| [Transaction-Timing Diagnostics in the CTMC Family](https://sheepdogprosperitypartners.com/continuous-time-markov-chains-transaction-timing/) | `stochastic_markov/` | `010_continuous_time_markov.py` | `010_continuous_time_markov.ipynb` |
| [Screening a State's Medicaid Market with Public Data](https://sheepdogprosperitypartners.com/screening-a-states-medicaid-market-with-public-data/) | `medicaid_public_data_screening/` | `screening-a-states-medicaid-market-with-public-data.py` | `screening-a-states-medicaid-market-with-public-data.ipynb` |
| [Medicare Outlier Screen](https://sheepdogprosperitypartners.com/medicare-outlier-screen/) | `medicare_outlier_screen/` | `medicare_outlier_screen.py` | `medicare_outlier_screen.ipynb` |
| Beyond Benford's Law, pending publication | `forensic_numeric_techniques/` | `beyond-benford-fraud-detection-techniques.py` | `beyond-benford-fraud-detection-techniques.ipynb` |
| [CFIUS: The Inbound Capital Screen](https://sheepdogprosperitypartners.com/cfius-inbound-capital-screen/) | `national_security_diligence/notebooks/` | `A1_cfius_public_actions.py` | `A1_cfius_public_actions.ipynb` |
| [Outbound Investment Security: The Reverse CFIUS](https://sheepdogprosperitypartners.com/outbound-investment-reverse-cfius/) | `national_security_diligence/notebooks/` | `A2_outbound_triage.py` | `A2_outbound_triage.ipynb` |
| [The DOJ Data Security Program](https://sheepdogprosperitypartners.com/data-security-program-eo-14117/) | `national_security_diligence/notebooks/` | `C1_data_threshold_checker.py` | `C1_data_threshold_checker.ipynb` |
| [Asset Seizure and Forfeiture](https://sheepdogprosperitypartners.com/asset-seizure-forfeiture-enforcement-spine/) | `national_security_diligence/notebooks/` | `C2_forfeiture_timeline_builder.py` | `C2_forfeiture_timeline_builder.ipynb` |
| [The Whistleblower and Bounty Bridge](https://sheepdogprosperitypartners.com/whistleblower-bounty-national-security/) | `national_security_diligence/notebooks/` | `C3_bounty_program_matrix.py` | `C3_bounty_program_matrix.ipynb` |
| [The Integrated National-Security Diligence Workflow](https://sheepdogprosperitypartners.com/national-security-diligence-workflow/) | `national_security_diligence/notebooks/` | `D1_integrated_workflow.py` | `D1_integrated_workflow.ipynb` |
| [The Screening Toolkit](https://sheepdogprosperitypartners.com/national-security-screening-toolkit/) | `national_security_diligence/notebooks/` | `D2_screening_toolkit.py` | `D2_screening_toolkit.ipynb` |
| [Forced Divestiture vs. Forfeiture](https://sheepdogprosperitypartners.com/divestiture-vs-forfeiture-anatomy/) | `national_security_diligence/notebooks/` | `D3_remedy_comparison_timeline.py` | `D3_remedy_comparison_timeline.ipynb` |
| Cross-Border Open-Source Diligence Atlas, pending publication | `cross_border_diligence_atlas/notebooks/` | `BR_01_entity_registry_screen.py` | `BR_01_entity_registry_screen.ipynb` |
| Cross-Border Open-Source Diligence Atlas, pending publication | `cross_border_diligence_atlas/notebooks/` | `BR_02_sanctions_procurement_crosscheck.py` | `BR_02_sanctions_procurement_crosscheck.ipynb` |
| Cross-Border Open-Source Diligence Atlas, pending publication | `cross_border_diligence_atlas/notebooks/` | `AR_01_rns_entity_screen.py` | `AR_01_rns_entity_screen.ipynb` |
| Cross-Border Open-Source Diligence Atlas, pending publication | `cross_border_diligence_atlas/notebooks/` | `AR_02_boletin_timeline_builder.py` | `AR_02_boletin_timeline_builder.ipynb` |
| Cross-Border Open-Source Diligence Atlas, pending publication | `cross_border_diligence_atlas/notebooks/` | `US_memo_country_risk_flags.py` | `US_memo_country_risk_flags.ipynb` |

## Run

Create a Python 3.10 or newer environment, then install the dependency set needed for the companion you are running. The stochastic Markov companions use `numpy`, `pandas`, `scipy`, `statsmodels`, `arch`, and `hmmlearn`. Public-data companions may also use `requests`, `duckdb`, and notebook tooling.

Example:

```bash
python stochastic_markov/008_two_stage_screen.py
```

For notebook review:

```bash
jupyter nbconvert --execute --to notebook --inplace stochastic_markov/008_two_stage_screen.ipynb
```

## Repository Policy

The duality rule is enforced by `tools/check_duality.py` and the workflow in `.github/workflows/duality-check.yml`.

Large public-data files such as Parquet downloads, DuckDB files, generated provider caches, and live bulk-list pulls are ignored. Small synthetic, sample, or redacted CSV fixtures under `data/sample/`, `data/synthetic/`, and `data/redacted_outputs/` may be tracked when they are needed for a notebook to run offline.

## License

MIT. Use, modify, and fork freely. Attribution to Noah Green CPA CFE and the DD Tech Lab publication is appreciated but not required.
