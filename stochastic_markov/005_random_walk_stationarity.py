#!/usr/bin/env python3
"""Companion artifact for DD Tech Lab Stochastic / Markov Article 005.

Random-walk and stationarity tests on account reconciliations.

The script combines Augmented Dickey-Fuller, KPSS, four-quadrant drift
classification, synthetic reconciliation series, and a paired-account
cointegration example into one deterministic companion file.

Run:
    python 005_random_walk_stationarity.py
"""

from __future__ import annotations

import warnings

import numpy as np
import pandas as pd
from statsmodels.tsa.stattools import adfuller, coint, kpss


N_MONTHS = 36


def adf_test_diagnostic(series: pd.Series, alpha: float = 0.05) -> dict:
    """ADF test with AIC-selected lag length and constant plus trend regression."""
    stat, p, used_lag, n_obs, crit_values, _ = adfuller(
        series.dropna().values, autolag="AIC", regression="ct"
    )
    return {
        "test": "ADF",
        "statistic": float(stat),
        "p_value": float(p),
        "used_lag": int(used_lag),
        "n_observations": int(n_obs),
        "critical_values": {k: float(v) for k, v in crit_values.items()},
        "reject_unit_root": p < alpha,
    }


def kpss_test_diagnostic(
    series: pd.Series, alpha: float = 0.05, regression: str = "c"
) -> dict:
    """KPSS test with auto-selected lag and constant or trend regression."""
    stat, p, used_lag, crit_values = kpss(
        series.dropna().values, regression=regression, nlags="auto"
    )
    return {
        "test": "KPSS",
        "statistic": float(stat),
        "p_value": float(p),
        "used_lag": int(used_lag),
        "regression": regression,
        "critical_values": {k: float(v) for k, v in crit_values.items()},
        "reject_stationarity": p < alpha,
    }


def reconciliation_drift_diagnostic(
    series: pd.Series, alpha: float = 0.05, kpss_regression: str = "c"
) -> dict:
    """Combined ADF and KPSS four-quadrant diagnostic for balance drift."""
    adf_result = adf_test_diagnostic(series, alpha)
    kpss_result = kpss_test_diagnostic(series, alpha, regression=kpss_regression)

    if adf_result["reject_unit_root"] and not kpss_result["reject_stationarity"]:
        diagnosis = "stationary"
        action = "no_audit_action"
    elif not adf_result["reject_unit_root"] and kpss_result["reject_stationarity"]:
        diagnosis = "drift_unit_root"
        action = "investigation_warranted"
    elif adf_result["reject_unit_root"] and kpss_result["reject_stationarity"]:
        diagnosis = "inconclusive_high"
        action = "investigate_inconclusive"
    else:
        diagnosis = "inconclusive_low"
        action = "extend_series_or_alternative_test"

    return {
        "adf": adf_result,
        "kpss": kpss_result,
        "diagnosis": diagnosis,
        "action": action,
        "n_observations": int(series.dropna().shape[0]),
    }


def generate_clean_series(n: int, seed: int = 1) -> pd.Series:
    """Stationary AR(1) with rho = 0.4."""
    rng = np.random.default_rng(seed)
    eps = rng.standard_normal(n)
    x = np.zeros(n)
    for t in range(1, n):
        x[t] = 0.4 * x[t - 1] + eps[t]
    return pd.Series(x)


def generate_gradual_drift(n: int, seed: int = 2) -> pd.Series:
    """Random walk with small upward drift."""
    rng = np.random.default_rng(seed)
    return pd.Series(np.cumsum(rng.standard_normal(n) + 0.15))


def generate_step_change(
    n: int, seed: int = 3, step_month: int = 18, step_size: float = 5.0
) -> pd.Series:
    """Stationary AR(1) baseline with a deterministic step jump."""
    rng = np.random.default_rng(seed)
    eps = rng.standard_normal(n)
    x = np.zeros(n)
    for t in range(1, n):
        x[t] = 0.4 * x[t - 1] + eps[t]
    x[step_month:] += step_size
    return pd.Series(x)


def paired_account_cointegration(
    series_a: pd.Series, series_b: pd.Series, alpha: float = 0.05
) -> dict:
    """Engle-Granger cointegration test on a paired-account series."""
    aligned = pd.concat([series_a, series_b], axis=1).dropna()
    if aligned.shape[0] < 25:
        return {"warning": "insufficient_data", "n_observations": aligned.shape[0]}
    stat, p, crit = coint(aligned.iloc[:, 0], aligned.iloc[:, 1])
    return {
        "test": "Engle-Granger cointegration",
        "statistic": float(stat),
        "p_value": float(p),
        "critical_values": {
            "1%": float(crit[0]),
            "5%": float(crit[1]),
            "10%": float(crit[2]),
        },
        "reject_no_cointegration": p < alpha,
        "n_observations": int(aligned.shape[0]),
    }


def main() -> None:
    warnings.filterwarnings("ignore")
    print("=" * 78)
    print("DD Tech Lab Stochastic Article 005, companion artifact")
    print("Random-walk and stationarity tests on account reconciliations")
    print("=" * 78)

    clean = generate_clean_series(N_MONTHS)
    drift = generate_gradual_drift(N_MONTHS)
    step = generate_step_change(N_MONTHS)

    print("\nFour-quadrant ADF plus KPSS diagnostic")
    for label, series in [
        ("clean", clean),
        ("gradual_drift", drift),
        ("step_change", step),
    ]:
        result = reconciliation_drift_diagnostic(series)
        print(
            f"{label:<15} | diagnosis={result['diagnosis']:<22} "
            f"| ADF p={result['adf']['p_value']:.4f} "
            f"| KPSS p={result['kpss']['p_value']:.4f}"
        )

    print("\nFirst five synthetic values")
    print("clean:", [round(x, 4) for x in clean.head().tolist()])
    print("gradual_drift:", [round(x, 4) for x in drift.head().tolist()])
    print("step_change:", [round(x, 4) for x in step.head().tolist()])

    paired = paired_account_cointegration(clean.cumsum(), clean.cumsum() + step * 0.05)
    print("\nPaired-account cointegration check")
    print(f"p-value: {paired['p_value']:.4f}")
    print(f"reject no cointegration: {paired['reject_no_cointegration']}")


if __name__ == "__main__":
    main()
