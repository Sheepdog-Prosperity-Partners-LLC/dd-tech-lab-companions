#!/usr/bin/env python3
import numpy as np
from scipy.stats import chisquare
from scipy.stats import chi2 as chi2_dist

N_STATES = 5
N_TRANSACTIONS = 5000


def holm_adjust(pvals: np.ndarray, alpha: float = 0.05) -> tuple[np.ndarray, np.ndarray]:
    order = np.argsort(pvals)
    sorted_p = pvals[order]
    m = len(sorted_p)
    adjusted_sorted = np.empty(m, dtype=float)
    running_max = 0.0
    for i, p in enumerate(sorted_p):
        adjusted = (m - i) * p
        running_max = max(running_max, adjusted)
        adjusted_sorted[i] = min(running_max, 1.0)
    adjusted = np.empty(m, dtype=float)
    adjusted[order] = adjusted_sorted
    reject = adjusted <= alpha
    return reject, adjusted


def benford_first_digit_test(values: np.ndarray, alpha: float = 0.05) -> dict:
    expected_p = np.array([np.log10(1 + 1.0 / d) for d in range(1, 10)])
    nonzero = values[values != 0]
    first_digits = np.array([int(str(int(abs(v)))[0]) for v in nonzero])
    observed = np.array([(first_digits == d).sum() for d in range(1, 10)])
    expected = expected_p * observed.sum()
    chi2_stat, p_value = chisquare(observed, expected)
    return {'p_value': float(p_value), 'reject_benford': bool(p_value < alpha)}


def markov_transition_test(sequence: list[int], n_states: int, P_baseline: np.ndarray, alpha: float = 0.05) -> dict:
    N = np.zeros((n_states, n_states), dtype=int)
    for prev, curr in zip(sequence[:-1], sequence[1:]):
        N[prev, curr] += 1
    expected = N.sum(axis=1, keepdims=True) * P_baseline
    mask = expected > 0
    chi2_stat = float(((N[mask] - expected[mask]) ** 2 / expected[mask]).sum())
    active_predecessors = int((N.sum(axis=1) > 0).sum())
    df = max(active_predecessors * (n_states - 1), 1)
    p_value = 1.0 - chi2_dist.cdf(chi2_stat, df)
    return {'p_value': float(p_value), 'reject_baseline': bool(p_value < alpha)}


def two_stage_screen(values: np.ndarray, sequence: list[int], n_states: int,
                     P_baseline: np.ndarray, alpha: float = 0.05,
                     correction: str = 'holm') -> dict:
    benford = benford_first_digit_test(values, alpha)
    markov = markov_transition_test(sequence, n_states, P_baseline, alpha)
    pvals = np.array([benford['p_value'], markov['p_value']])
    if correction != 'holm':
        raise ValueError('This companion script implements Holm correction only.')
    reject, pvals_corrected = holm_adjust(pvals, alpha=alpha)
    return {
        'stage_1_benford': benford,
        'stage_2_markov': markov,
        'raw_p_values': pvals.tolist(),
        'adjusted_p_values': pvals_corrected.tolist(),
        'any_test_rejects': bool(reject.any()),
        'decision': 'investigate' if bool(reject.any()) else 'no_action',
    }


def generate_clean_data(n: int, seed: int) -> tuple[np.ndarray, list[int], np.ndarray]:
    rng = np.random.default_rng(seed)
    log_values = rng.uniform(np.log10(100), np.log10(100000), n)
    values = 10 ** log_values
    P_clean = np.array([
        [0.10, 0.20, 0.05, 0.55, 0.10],
        [0.20, 0.10, 0.05, 0.10, 0.55],
        [0.05, 0.05, 0.10, 0.40, 0.40],
        [0.55, 0.10, 0.05, 0.20, 0.10],
        [0.10, 0.55, 0.05, 0.10, 0.20],
    ])
    sequence = [int(rng.integers(N_STATES))]
    for _ in range(n - 1):
        sequence.append(int(rng.choice(N_STATES, p=P_clean[sequence[-1]])))
    return values, sequence, P_clean


def run_anomalous_example() -> None:
    clean_values, clean_seq, P_baseline = generate_clean_data(N_TRANSACTIONS, seed=42)
    rng_inject = np.random.default_rng(43)
    inject_idx = rng_inject.choice(N_TRANSACTIONS, 250, replace=False)
    clean_values[inject_idx[:125]] = 1000.0
    clean_values[inject_idx[125:]] = 10000.0
    clean_seq[2000:2150] = ([0, 1, 2, 3] * 38)[:150]
    result = two_stage_screen(clean_values, clean_seq, N_STATES, P_baseline, alpha=0.05, correction='holm')
    print('Anomalous file')
    print('Benford p-value:', f"{result['stage_1_benford']['p_value']:.6f}")
    print('Markov p-value:', f"{result['stage_2_markov']['p_value']:.6f}")
    print('Adjusted p-values:', [round(x, 6) for x in result['adjusted_p_values']])
    print('Decision:', result['decision'])


def run_false_positive_monte_carlo() -> None:
    _, _, P_baseline = generate_clean_data(2000, seed=42)
    n_simulations = 1000
    or_rejections = 0
    holm_rejections = 0
    for sim_seed in range(n_simulations):
        sim_values, sim_seq, _ = generate_clean_data(2000, seed=sim_seed)
        sim_result = two_stage_screen(sim_values, sim_seq, N_STATES, P_baseline, alpha=0.05)
        if sim_result['stage_1_benford']['p_value'] < 0.05 or sim_result['stage_2_markov']['p_value'] < 0.05:
            or_rejections += 1
        if sim_result['any_test_rejects']:
            holm_rejections += 1
    print('\nClean-data Monte Carlo')
    print('OR false-positive rate:', round(or_rejections / n_simulations, 4))
    print('Holm false-positive rate:', round(holm_rejections / n_simulations, 4))


if __name__ == '__main__':
    run_anomalous_example()
    run_false_positive_monte_carlo()
