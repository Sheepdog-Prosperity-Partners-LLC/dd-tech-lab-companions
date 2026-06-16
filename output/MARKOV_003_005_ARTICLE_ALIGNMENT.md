# Markov 003 and 005 Article Alignment

Prepared for the next WordPress edit pass. The companion code is the source of truth for these two examples.

## Runtime Used

Repository: `dd-tech-lab-companions`

Interpreter: repository virtual environment, Python 3.11.15

Relevant packages:

- `numpy 2.4.6`
- `pandas 3.0.3`
- `scipy 1.17.1`
- `statsmodels 0.14.6`
- `hmmlearn 0.3.3`

Commands:

```bash
.venv/bin/python stochastic_markov/003_hidden_markov_earnings_management.py
.venv/bin/python stochastic_markov/005_random_walk_stationarity.py
```

## 003 Hidden Markov Earnings Management

Old output line:

```text
Viterbi-decoded manipulation periods: precision=0.433, recall=0.625 (TP=60, FP=79, FN=36)
```

New output line:

```text
Viterbi-decoded manipulation periods: precision=0.048, recall=0.958 (TP=92, FP=1814, FN=4)
```

Old target:

Paragraph beginning:

```text
This performance, precision 0.433, recall 0.625
```

Replacement prose:

```text
This run produces precision 0.048 and recall 0.958 on the synthetic panel. The result is a high-sensitivity triage signal with many false positives, not a claim of field accuracy. It is useful as a workflow demonstration: the audit team can rank periods for review by posterior probability, then tune the review threshold to the engagement's cost tolerance. The caveat remains that synthetic-panel performance demonstrates workflow shape only; field accuracy depends on the entity's actual manipulation patterns and feature-engineering choices.
```

## 005 Random-Walk and Stationarity Tests

Old first-five values:

```text
clean[:5] = [0.0000, 0.6924, 1.2849, -0.1502, -0.4006]
drift[:5] = [0.2300, 1.7104, 1.6839, 3.4262, 4.1108]
step_change[:5] = [0.0000, 1.0306, 0.6859, 0.6022, 0.7011]
```

New first-five values:

```text
clean[:5] = [0.0000, 0.8216, 0.6591, -1.0395, 0.4895]
gradual_drift[:5] = [0.3391, -0.0337, -0.2968, -2.5882, -0.6385]
step_change[:5] = [0.0000, -2.5557, -0.6042, -0.8094, -0.7764]
```

Old target:

Sentence classifying the clean series as `stationary`, gradual drift as `drift_unit_root`, and step change as `inconclusive_high`.

Replacement prose:

```text
With the specified seeds, the deterministic output classifies the clean series as stationary (ADF p=0.0206, KPSS p=0.1000), the gradual-drift series as inconclusive_high (ADF p=0.0397, KPSS p=0.0100), and the step-change series as drift_unit_root (ADF p=0.1111, KPSS p=0.0138). The gradual-drift result is the ambiguous one because both tests reject their nulls. The step-change result is an investigation signal in this 36-month sample, not a clean structural-break classification.
```

Insert after the paired-account helper:

```text
The paired-account check returns p-value 0.6609 and reject no cointegration = False, so this synthetic pair does not provide evidence of cointegration at alpha 0.05.
```
