# DD Tech Lab — Companion Code

Runnable Python companion artifacts for articles published at [sheepdogprosperitypartners.com/dd-tech-lab](https://sheepdogprosperitypartners.com/dd-tech-lab/).

Each script is self-contained, seeded for deterministic output (`np.random.seed(42)` or `np.random.default_rng(42)`), and consolidates the worked example from the corresponding article into a single end-to-end runnable file.

## Stochastic Processes & Markov Chains in Fraud Examination

| # | Article | Companion script |
|---|---|---|
| 001 | [First-Order Markov Modeling for Transaction-Stream Analysis in Audit](https://sheepdogprosperitypartners.com/why-markov-chains-belong-in-financial-statement-audit/) | [`stochastic_markov/001_markov_intro.py`](stochastic_markov/001_markov_intro.py) |
| 002 | [Modeling Journal-Entry Sequences in Production](https://sheepdogprosperitypartners.com/modeling-journal-entry-sequences-in-production/) | [`stochastic_markov/002_journal_entry_production.py`](stochastic_markov/002_journal_entry_production.py) |
| 003 | [Hidden Markov Models for Earnings-Management Regime Detection](https://sheepdogprosperitypartners.com/hidden-markov-models-earnings-management-regime-detection/) | _Companion in progress; see article for full code listings_ |
| 004 | [Markov Mixture Models for Round-Tripping and Lapping Detection](https://sheepdogprosperitypartners.com/markov-mixture-models-round-tripping-lapping/) | [`stochastic_markov/004_mixture_round_tripping.py`](stochastic_markov/004_mixture_round_tripping.py) |
| 005 | [Random-Walk and Stationarity Tests on Account Reconciliations](https://sheepdogprosperitypartners.com/random-walk-stationarity-tests-account-reconciliations/) | _Companion in progress; see article for full code listings_ |
| 006 | [Markov Decision Processes for Risk-Based Audit Sampling](https://sheepdogprosperitypartners.com/markov-decision-processes-risk-based-audit-sampling/) | [`stochastic_markov/006_markov_decision_audit_sampling.py`](stochastic_markov/006_markov_decision_audit_sampling.py) |
| 007 | [Stochastic Volatility Models for Restatement-Timing Anomalies](https://sheepdogprosperitypartners.com/stochastic-volatility-restatement-timing/) | [`stochastic_markov/007_garch_restatement_timing.py`](stochastic_markov/007_garch_restatement_timing.py) |
| 008 | [Two-Stage Screening: Benford's Law + First-Order Markov](https://sheepdogprosperitypartners.com/two-stage-screening-benford-first-order-markov/) | [`stochastic_markov/008_two_stage_screen.py`](stochastic_markov/008_two_stage_screen.py) |
| 009 | [Higher-Order and Variable-Order Markov Models for Long-Memory Fraud Schemes](https://sheepdogprosperitypartners.com/higher-order-variable-order-markov-long-memory/) | [`stochastic_markov/009_higher_order_variable_order_markov.py`](stochastic_markov/009_higher_order_variable_order_markov.py) |
| 010 | [Transaction-Timing Diagnostics in the CTMC Family](https://sheepdogprosperitypartners.com/continuous-time-markov-chains-transaction-timing/) | [`stochastic_markov/010_continuous_time_markov.py`](stochastic_markov/010_continuous_time_markov.py) |

## How to run

Standard Python 3.10+ environment with `numpy`, `pandas`, `scipy`, `statsmodels`. Article 007 additionally needs `arch`. Install everything via:

```bash
pip install numpy pandas scipy statsmodels arch hmmlearn
```

Then run any companion:

```bash
python stochastic_markov/008_two_stage_screen.py
```

Each script prints its deterministic output to stdout. The printed output matches the numbers cited in the corresponding article.

## License

MIT. Use, modify, fork freely. Attribution to Noah Green CPA CFE and the DD Tech Lab publication is appreciated but not required.

## About

Prepared by Noah Green CPA CFE. DD Tech Lab is the technical-methods publication of Sheepdog Prosperity Partners.
