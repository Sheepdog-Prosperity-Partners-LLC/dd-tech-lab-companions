#!/usr/bin/env python3
"""Companion artifact for DD Tech Lab Stochastic / Markov Article 001,
First-Order Markov Modeling for Transaction-Stream Analysis in Audit.

End-to-end reproducible script. Generates 950 baseline transactions and injects
a 50-state round-tripping cycle on a 5-state account-class chain (Cash, AR,
Revenue, COGS, Inventory). Computes the empirical transition matrix, Frobenius
distance vs baseline, chi-squared statistic with audit-context degrees of
freedom, and the cell-level standardized-residual diagnostic map.

Audience:    audit-portfolio risk officers, DD analysts, CPAs/CFEs/CFFs
             building first-order Markov journal-entry diagnostics.
Reproducibility: deterministic under seed=42. Print output is the source of
             truth for the article's reported numbers.
Run:         python 001_markov_intro.py
"""
import numpy as np
import pandas as pd
from scipy.stats import chi2 as chi2_dist


# =============================================================================
# Core helpers
# =============================================================================
def transition_matrix(sequence, states):
    """Empirical first-order transition matrix from a state sequence.

    Returns (P_hat, N) where P_hat is row-stochastic and N is the count matrix.
    """
    idx = {s: i for i, s in enumerate(states)}
    n = len(states)
    N = np.zeros((n, n), dtype=int)
    for prev, curr in zip(sequence[:-1], sequence[1:]):
        N[idx[prev], idx[curr]] += 1
    row_sums = N.sum(axis=1, keepdims=True)
    with np.errstate(invalid="ignore", divide="ignore"):
        P_hat = np.where(row_sums > 0, N / row_sums, 0.0)
    return P_hat, N


def sample_chain(P, states, n, start=0):
    """Sample n states from a Markov chain; returns n labels (n-1 transitions)."""
    seq = [start]
    for _ in range(n - 1):
        seq.append(np.random.choice(len(states), p=P[seq[-1]]))
    return [states[s] for s in seq]


def chi2_transition_test(N, E):
    """Chi-squared goodness-of-fit against an externally-specified baseline P^(0).

    df = active_predecessor_states * (n_states - 1). Cells with E = 0 are
    excluded. Small-cell warning per Cochran's rule (E < 5 in any cell).
    """
    mask = E > 0
    chi2_stat = float(((N[mask] - E[mask]) ** 2 / E[mask]).sum())
    active_rows = int((N.sum(axis=1) > 0).sum())
    df = max(active_rows * (N.shape[1] - 1), 1)
    p_value = float(1.0 - chi2_dist.cdf(chi2_stat, df))
    small_cells = int((E[mask] < 5).sum())
    return {
        "chi2_statistic": chi2_stat,
        "degrees_of_freedom": df,
        "p_value_asymptotic": p_value,
        "n_small_expected_cells": small_cells,
        "cochran_warning": small_cells > 0,
    }


# =============================================================================
# Main worked example
# =============================================================================
def main():
    np.random.seed(42)

    states = ["Cash", "AR", "Revenue", "COGS", "Inventory"]
    P_baseline = np.array([
        [0.10, 0.10, 0.05, 0.05, 0.70],
        [0.60, 0.05, 0.30, 0.03, 0.02],
        [0.10, 0.70, 0.05, 0.10, 0.05],
        [0.05, 0.02, 0.03, 0.15, 0.75],
        [0.20, 0.05, 0.10, 0.55, 0.10],
    ])
    assert np.allclose(P_baseline.sum(axis=1), 1.0)

    print("=" * 70)
    print("DD Tech Lab Stochastic Article 001, companion artifact")
    print("=" * 70)

    # 950 baseline states (clean Markov-chain sampling)
    baseline_seq = sample_chain(P_baseline, states, 950)

    # 50-state round-tripping injection (Revenue → AR → Cash → COGS cycle)
    round_trip = (["Revenue", "AR", "Cash", "COGS"] * 13)[:50]
    observed_seq = baseline_seq + round_trip

    print(f"\nGenerated 1,000-state observed_seq (950 baseline + 50 round-trip)")
    print(f"  first 5 states: {observed_seq[:5]}")
    print(f"  last 5 states (tail of round-trip): {observed_seq[-5:]}")

    P_obs, N_obs = transition_matrix(observed_seq, states)
    expected = N_obs.sum(axis=1, keepdims=True) * P_baseline

    # Frobenius distance
    d_F = float(np.linalg.norm(P_obs - P_baseline, ord="fro"))
    print(f"\nFrobenius distance ||P_obs - P_baseline||_F = {d_F:.4f}")

    # Chi-squared test
    result = chi2_transition_test(N_obs, expected)
    print(f"\nChi-squared test against baseline P^(0):")
    print(f"  statistic = {result['chi2_statistic']:.2f}")
    print(f"  df = {result['degrees_of_freedom']}")
    print(f"  p-value (asymptotic) = {result['p_value_asymptotic']:.6f}")
    if result["cochran_warning"]:
        print(f"  WARNING: {result['n_small_expected_cells']} cells have E < 5")

    # Standardized residual map
    mask = expected > 0
    residuals = np.zeros_like(expected, dtype=float)
    residuals[mask] = (N_obs[mask] - expected[mask]) / np.sqrt(expected[mask])
    print(f"\nStandardized residual map (|z| > 2 indicates anomalous cells):")
    print(pd.DataFrame(residuals, index=states, columns=states).round(2))

    print("\n" + "=" * 70)
    print("Workpaper artifact: cells with |residual| > 2 direct substantive")
    print("procedures (AS 2401 §60 journal-entry testing) at the specific")
    print("transitions the round-tripping pattern over-represents.")
    print("=" * 70)


if __name__ == "__main__":
    main()
