# Beyond Benford's Law: a Hands-On Tour of Fraud-Detection Techniques

Runnable notebook companion for the DD Tech Lab article:

- Article hub: <https://sheepdogprosperitypartners.com/dd-tech-lab/>
- Notebook: [`beyond-benford-fraud-detection-techniques.ipynb`](beyond-benford-fraud-detection-techniques.ipynb)

Benford's Law is the famous one, but it is a single lens. This notebook walks through the wider battery of numerical tests a buyer can run in due diligence, grouped into four families:

- Reading the digits: Benford first-digit, first and last two digits, round-number bias, relative size factor, digit preference.
- Reading the structure: duplicate and split payments, threshold bunching, sequence integrity, the impossible-cell check.
- Reading distribution and flow: rank-frequency (Zipf), novelty-decay, round-tripping, ghost-vendor cross-match.
- Reading timing and the whole company: period-end cutoff, posting-time anomalies, the Altman Z-score and Beneish M-score, multivariate outliers, memo text analytics.

The unifying idea is convergence: no single test is proof, and the signal worth chasing is a transaction caught by several independent tests at once.

## How to run

No third-party packages are required. Every cell uses only the Python standard library.

```bash
jupyter notebook beyond-benford-fraud-detection-techniques.ipynb
```

Each cell is self-contained and carries its own small, made-up dataset chosen to trip the test, so you can see what a flag looks like. The notebook ships with its outputs included because all data is synthetic. There is no real-world data, so there is no public-data hygiene concern.

The code is illustrative and uses synthetic data only. It makes no allegation about any person or entity.
