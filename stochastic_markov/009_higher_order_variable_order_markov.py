#!/usr/bin/env python3
"""Companion artifact for DD Tech Lab Stochastic / Markov Article 009,
Higher-Order and Variable-Order Markov Models for Long-Memory Fraud Schemes.

End-to-end reproducible script. Consolidates the k-th-order Markov fitter,
the BIC selection function, the PST (Probabilistic Suffix Tree) construction
and summary, the synthetic-data generator (clean baseline + injected lapping),
and the false-positive-rate quantification loop into one runnable script.

PEDAGOGICAL implementation. The PST build runs in O(T^2 * D * |S|) due to
linear-time suffix lookup; production deployment on real audit ledgers should
swap the find_positions helper for an Ukkonen suffix-tree construction to get
O(T) total runtime. See article body for the production migration note.

Audience:    FA-DD analysts, forensic-accounting investigators, FBI Forensic
             Accountants, and audit managers (CPAs/CFEs/CFFs) working long-
             memory fraud schemes (lapping, kiting, multi-quarter rotations).
Reproducibility: deterministic under np.random.seed(42).
Run:         python 009_higher_order_variable_order_markov.py
"""
import numpy as np


# =============================================================================
# k-th-order Markov fitter + BIC selection
# =============================================================================
def fit_kth_order_markov(sequence, n_states, k=2):
    """Estimate a k-th-order Markov transition tensor from a sequence."""
    shape = (n_states,) * (k + 1)
    counts = np.zeros(shape, dtype=int)
    for i in range(len(sequence) - k):
        idx = tuple(sequence[i:i + k + 1])
        counts[idx] += 1
    sums = counts.sum(axis=-1, keepdims=True)
    with np.errstate(invalid="ignore", divide="ignore"):
        P = np.where(sums > 0, counts / sums, 0.0)
    return P, counts


def log_likelihood_kth_order(sequence, n_states, k):
    """Log-likelihood under the fitted k-th-order tensor (empirical MLE)."""
    P, counts = fit_kth_order_markov(sequence, n_states, k)
    with np.errstate(divide="ignore"):
        log_P = np.where(P > 0, np.log(P), 0.0)
    return float((counts * log_P).sum())


def select_markov_order(sequence, n_states, k_candidates=(1, 2, 3, 4, 5)):
    """BIC-based selection of Markov order from a candidate set.

    BIC(k) = -2 * log_likelihood + n_params * log(n_eff - k)
    where n_params = |S|^k * (|S| - 1) and n_eff is the sequence length.
    """
    n_eff = len(sequence)
    results = []
    best_k, best_bic = None, np.inf
    for k in k_candidates:
        log_lik = log_likelihood_kth_order(sequence, n_states, k)
        n_params = (n_states ** k) * (n_states - 1)
        bic = -2 * log_lik + n_params * np.log(n_eff - k)
        results.append({"k": k, "log_likelihood": log_lik,
                        "n_params": n_params, "bic": bic})
        if bic < best_bic:
            best_k, best_bic = k, bic
    return {"selected_k": best_k, "selected_bic": best_bic, "all_results": results}


# =============================================================================
# PST (Probabilistic Suffix Tree) construction
# =============================================================================
class PSTNode:
    """Node in a probabilistic suffix tree."""
    def __init__(self, suffix, distribution, n_occurrences):
        self.suffix = suffix
        self.distribution = distribution
        self.n_occurrences = n_occurrences
        self.children = {}


def empirical_root_distribution(sequence, n_states, alpha_smooth=0.5):
    """Marginal next-state distribution with Laplace add-alpha smoothing."""
    counts = np.bincount(sequence, minlength=n_states).astype(float)
    smoothed = counts + alpha_smooth
    return smoothed / smoothed.sum()


def kl_divergence_smoothed(p_counts, q_dist, n_states, alpha_smooth=0.5):
    """KL(p_smooth || q_smooth) with Laplace add-alpha smoothing for stability."""
    n_p = float(p_counts.sum())
    p_smooth = (p_counts + alpha_smooth) / (n_p + alpha_smooth * n_states)
    q_effective_counts = q_dist * n_p
    q_smooth = (q_effective_counts + alpha_smooth) / (n_p + alpha_smooth * n_states)
    return float(np.sum(p_smooth * np.log(p_smooth / q_smooth)))


def build_pst(sequence, n_states, max_depth=5, min_count=10,
                divergence_threshold=0.15, alpha_smooth=0.5):
    """Build a probabilistic suffix tree by greedy context extension.

    Pedagogical O(T^2 * D * |S|) implementation. See module docstring for
    production migration to Ukkonen suffix tree.
    """
    root_dist = empirical_root_distribution(sequence, n_states, alpha_smooth)
    root = PSTNode(suffix=(), distribution=root_dist,
                    n_occurrences=max(len(sequence) - 1, 1))

    def find_positions(suffix):
        if not suffix:
            return list(range(len(sequence) - 1))
        d = len(suffix)
        positions = []
        for i in range(d - 1, len(sequence) - 1):
            match = True
            for j in range(d):
                if sequence[i - j] != suffix[j]:
                    match = False
                    break
            if match:
                positions.append(i)
        return positions

    def extend_node(node, depth):
        if depth >= max_depth:
            return
        for extending_state in range(n_states):
            extended_suffix = (extending_state,) + node.suffix
            positions = find_positions(extended_suffix)
            if len(positions) < min_count:
                continue
            next_states = np.array([sequence[i + 1] for i in positions])
            cond_counts = np.bincount(next_states, minlength=n_states).astype(float)
            cond_smoothed = cond_counts + alpha_smooth
            cond_dist = cond_smoothed / cond_smoothed.sum()
            kl = kl_divergence_smoothed(cond_counts, node.distribution, n_states, alpha_smooth)
            if kl > divergence_threshold:
                child = PSTNode(suffix=extended_suffix, distribution=cond_dist,
                                  n_occurrences=len(positions))
                node.children[extending_state] = child
                extend_node(child, depth + 1)

    extend_node(root, depth=0)
    return root


def pst_tree_summary(root, indent=0):
    """Pretty-print the PST structure for inspection."""
    lines = ["  " * indent + f"suffix={root.suffix or '(root)'}, "
                              f"n={root.n_occurrences}, "
                              f"dist={np.round(root.distribution, 2).tolist()}"]
    for child in root.children.values():
        lines.extend(pst_tree_summary(child, indent + 1))
    return lines


# =============================================================================
# Synthetic data generation: clean baseline + injected lapping
# =============================================================================
N_STATES = 6  # 5 customers + 1 cash state
T = 2000  # longer sequence so BIC can support higher-order detection
N_CUSTOMERS = 5

# Clean baseline: customers transition mostly to cash; cash returns roughly uniformly
P_CLEAN = np.full((N_STATES, N_STATES), 0.10)
for c in range(N_CUSTOMERS):
    P_CLEAN[c] = [0.10] * N_CUSTOMERS + [0.50]
    P_CLEAN[c] /= P_CLEAN[c].sum()
P_CLEAN[-1] = [0.20] * N_CUSTOMERS + [0.0]
P_CLEAN[-1] /= P_CLEAN[-1].sum()


def sample_clean_sequence(T):
    seq = [int(np.random.randint(N_STATES))]
    for _ in range(T - 1):
        seq.append(int(np.random.choice(N_STATES, p=P_CLEAN[seq[-1]])))
    return seq


def inject_lapping(sequence, inject_start, n_cycles):
    """Inject a 5-state lapping cycle: cust_A → B → C → D → cash → repeat."""
    cycle = [0, 1, 2, 3, 5] * n_cycles
    new_seq = sequence.copy()
    new_seq[inject_start:inject_start + len(cycle)] = cycle
    return new_seq


# =============================================================================
# Main
# =============================================================================
def main():
    np.random.seed(42)
    print("=" * 78)
    print("DD Tech Lab Stochastic Article 009, companion artifact")
    print("Higher-Order + Variable-Order Markov for Long-Memory Fraud Schemes")
    print("=" * 78)

    # Generate the two test sequences. Lapping injection runs ~75% of the sequence
    # so BIC has enough higher-order signal to upgrade past k=1.
    clean_seq = sample_clean_sequence(T)
    lapping_seq = inject_lapping(clean_seq, inject_start=200, n_cycles=300)
    print(f"\n[Step 1] Synthetic sequences: T={T} states each, N_STATES={N_STATES}")

    # BIC selection on both
    clean_sel = select_markov_order(clean_seq, N_STATES)
    lap_sel = select_markov_order(lapping_seq, N_STATES)
    print(f"\n[Step 2] BIC-selected k:")
    print(f"  clean: k = {clean_sel['selected_k']}")
    print(f"    BIC values: {[(r['k'], round(r['bic'], 1)) for r in clean_sel['all_results']]}")
    print(f"  lapping: k = {lap_sel['selected_k']}")
    print(f"    BIC values: {[(r['k'], round(r['bic'], 1)) for r in lap_sel['all_results']]}")

    # PST construction
    print(f"\n[Step 3] PST construction:")
    pst_clean = build_pst(clean_seq, N_STATES, max_depth=4, min_count=10,
                            divergence_threshold=0.15)
    pst_lap = build_pst(lapping_seq, N_STATES, max_depth=4, min_count=10,
                          divergence_threshold=0.15)
    clean_tree = pst_tree_summary(pst_clean)
    lap_tree = pst_tree_summary(pst_lap)
    print(f"  clean PST nodes: {len(clean_tree)}")
    print(f"  lapping PST nodes: {len(lap_tree)}")

    # False-positive quantification loop
    print(f"\n[Step 4] False-positive quantification (100 clean replicates, seeds 43-142):")
    fp_k = []
    fp_pst = []
    for seed_offset in range(1, 101):
        np.random.seed(42 + seed_offset)
        fp_seq = sample_clean_sequence(T)
        fp_sel = select_markov_order(fp_seq, N_STATES)
        fp_k.append(fp_sel["selected_k"])
        fp_pst_tree = build_pst(fp_seq, N_STATES, max_depth=4, min_count=10,
                                  divergence_threshold=0.15)
        fp_pst.append(len(pst_tree_summary(fp_pst_tree)))

    k_counts = {k: fp_k.count(k) for k in sorted(set(fp_k))}
    print(f"  k-selection distribution: {k_counts}")
    print(f"  PST size, mean: {np.mean(fp_pst):.2f}, std: {np.std(fp_pst):.2f}")
    print(f"  PST size 95th percentile: {int(np.percentile(fp_pst, 95))}")
    print(f"  Lapping PST size ({len(lap_tree)}) vs 95p threshold: "
          f"{'EXCEEDS' if len(lap_tree) > np.percentile(fp_pst, 95) else 'within'}")

    print("\n" + "=" * 78)
    print("Workpaper artifact: BIC table + PST tree summary + false-positive 95p")
    print("threshold = engagement-team's substantive-procedure scope-expansion record")
    print("under PCAOB AS 2401 §A.5 and AS 1215.")
    print("=" * 78)


if __name__ == "__main__":
    main()
