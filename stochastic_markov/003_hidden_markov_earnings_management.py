#!/usr/bin/env python3
"""Companion artifact for DD Tech Lab Stochastic / Markov Article 003.

Hidden Markov model earnings-management regime detection on synthetic
public-company panel data.

The script uses one independent random generator per firm so adding or removing
firms does not perturb the data for unchanged firms. It fits a two-regime
Gaussian HMM per firm, applies a likelihood-ratio gate against a single-Gaussian
null, standardizes the manipulated state label, and prints the detection
performance workpaper line.

Run:
    python 003_hidden_markov_earnings_management.py
"""

from __future__ import annotations

import warnings

import numpy as np
from hmmlearn import hmm
from scipy.stats import chi2 as chi2_dist


N_FIRMS = 50
N_QUARTERS = 100
N_FEATURES = 6
N_MANIPULATED = 8

MU_CLEAN = np.zeros(N_FEATURES)
MU_MANIPULATED = np.array([1.5, 1.2, 0.8, 0.5, 0.3, -0.7])
MANIPULATION_DIRECTION = MU_MANIPULATED - MU_CLEAN


def generate_firm_quarter_panel(
    firm_idx: int, manipulation_window: tuple[int, int] | None
) -> np.ndarray:
    """Generate 100 quarters of features for one synthetic firm."""
    rng = np.random.default_rng(seed=firm_idx)
    features = rng.standard_normal((N_QUARTERS, N_FEATURES)) + MU_CLEAN
    if manipulation_window is not None:
        start, end = manipulation_window
        features[start:end] = (
            rng.standard_normal((end - start, N_FEATURES)) * 0.7 + MU_MANIPULATED
        )
    return features


def build_panel() -> tuple[np.ndarray, np.ndarray]:
    """Build a 50-firm panel and the matching ground-truth regime labels."""
    panel = []
    truth = []
    for firm in range(N_FIRMS):
        if firm < N_MANIPULATED:
            start = 30 + firm * 5
            end = start + 12
            panel.append(generate_firm_quarter_panel(firm, (start, end)))
            truth_firm = np.zeros(N_QUARTERS, dtype=int)
            truth_firm[start:end] = 1
        else:
            panel.append(generate_firm_quarter_panel(firm, None))
            truth_firm = np.zeros(N_QUARTERS, dtype=int)
        truth.append(truth_firm)
    return np.stack(panel), np.stack(truth)


def fit_two_regime_hmm(features_firm: np.ndarray, n_restarts: int = 10) -> tuple:
    """Fit a two-state Gaussian HMM with restart and covariance fallback."""
    best_ll, best_model, cov_type = -np.inf, None, "full"

    for restart in range(n_restarts):
        if restart == 3 and best_model is None:
            cov_type = "diag"
            warnings.warn(
                "Switching to covariance_type='diag' after full-covariance failures.",
                RuntimeWarning,
            )

        model = hmm.GaussianHMM(
            n_components=2,
            covariance_type=cov_type,
            n_iter=200,
            random_state=42 + restart,
            tol=1e-4,
        )
        try:
            model.fit(features_firm)
            ll = model.score(features_firm)
            if ll > best_ll:
                best_ll, best_model = ll, model
        except (ValueError, np.linalg.LinAlgError):
            continue

    return best_model, best_ll, cov_type


def null_model_loglikelihood(features: np.ndarray) -> float:
    """Log-likelihood under a single-Gaussian no-regime-switching null."""
    mu = features.mean(axis=0)
    cov = np.cov(features, rowvar=False) + np.eye(features.shape[1]) * 1e-8
    diff = features - mu
    log_det = float(np.linalg.slogdet(cov)[1])
    d = features.shape[1]
    quad = np.einsum("ti,ij,tj->t", diff, np.linalg.inv(cov), diff)
    return float((-0.5 * (d * np.log(2 * np.pi) + log_det + quad)).sum())


LRT_DF = 1 + 2 + N_FEATURES + N_FEATURES * (N_FEATURES + 1) // 2
LRT_ALPHA = 0.01
LRT_CRITICAL_LL_GAIN = chi2_dist.ppf(1 - LRT_ALPHA, LRT_DF) / 2.0


def standardize_manipulated_state(model, viterbi: np.ndarray, posterior: np.ndarray) -> tuple:
    """Return labels where state 1 is the manipulated-regime state."""
    proj_0 = np.dot(model.means_[0], MANIPULATION_DIRECTION)
    proj_1 = np.dot(model.means_[1], MANIPULATION_DIRECTION)

    if np.abs(proj_0 - proj_1) < 1e-6:
        manipulated_state = 1 if model.means_[1, 0] > model.means_[0, 0] else 0
    else:
        manipulated_state = 1 if proj_1 > proj_0 else 0

    if manipulated_state == 0:
        return 1 - viterbi, posterior[:, ::-1]
    return viterbi, posterior


def precision_recall(predicted: np.ndarray, true_labels: np.ndarray) -> dict:
    """Compute precision, recall, and raw counts."""
    tp = int(((predicted == 1) & (true_labels == 1)).sum())
    fp = int(((predicted == 1) & (true_labels == 0)).sum())
    fn = int(((predicted == 0) & (true_labels == 1)).sum())
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    return {"precision": precision, "recall": recall, "tp": tp, "fp": fp, "fn": fn}


def main() -> None:
    print("=" * 78)
    print("DD Tech Lab Stochastic Article 003, companion artifact")
    print("Hidden Markov model earnings-management regime detection")
    print("=" * 78)

    panel, truth = build_panel()
    posteriors_per_firm = np.zeros((N_FIRMS, N_QUARTERS, 2))
    viterbi_per_firm = np.zeros((N_FIRMS, N_QUARTERS), dtype=int)

    for firm in range(N_FIRMS):
        model, ll, _ = fit_two_regime_hmm(panel[firm])
        null_ll = null_model_loglikelihood(panel[firm])

        if model is None or (ll - null_ll) < LRT_CRITICAL_LL_GAIN:
            warnings.warn(
                f"Firm {firm}: two-state HMM did not beat the alpha=0.01 "
                f"likelihood-ratio gate. Substituting a 50/50 regime prior.",
                RuntimeWarning,
            )
            posteriors_per_firm[firm, :, :] = 0.5
            viterbi_per_firm[firm, :] = 0
            continue

        posterior = model.predict_proba(panel[firm])
        viterbi = model.predict(panel[firm])
        viterbi, posterior = standardize_manipulated_state(model, viterbi, posterior)
        posteriors_per_firm[firm] = posterior
        viterbi_per_firm[firm] = viterbi

    results = precision_recall(viterbi_per_firm.flatten(), truth.flatten())
    print(
        "Viterbi-decoded manipulation periods: "
        f"precision={results['precision']:.3f}, "
        f"recall={results['recall']:.3f} "
        f"(TP={results['tp']}, FP={results['fp']}, FN={results['fn']})"
    )


if __name__ == "__main__":
    warnings.filterwarnings("ignore")
    main()
