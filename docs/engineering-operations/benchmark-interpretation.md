# Benchmark Interpretation Guide

CareerCraft includes a deterministic benchmark runner and a small synthetic
sample dataset. The sample is a smoke test for the evaluation pipeline; it is
not evidence of general hiring accuracy.

## Reported metrics

### Mean absolute error

Mean absolute error measures the average absolute distance between predicted
and labelled scores. Lower values are better for the evaluated dataset, but a
small value on a tiny synthetic sample does not prove real-world calibration.

### Pearson correlation

Pearson correlation measures linear association between predicted and labelled
scores. It can be high even when predictions have a consistent scale or offset
error.

### Spearman correlation

Spearman correlation measures whether examples are ranked in a similar order.
It does not show that the score values themselves are well calibrated.

## Responsible use

- Record the dataset version and command used for every comparison.
- Compare a proposed scoring change with the current baseline.
- Inspect per-pair results instead of relying on one aggregate metric.
- Do not tune against the smoke-test sample until the result looks artificially
  good.
- Keep semantic results separate when optional dependencies are unavailable.
- Do not describe synthetic metrics as employer validation or hiring accuracy.

## Evidence needed for broader claims

Broader quality claims require a larger, diverse, human-reviewed dataset with
documented labels, representative role families, privacy controls, and a
repeatable evaluation protocol.
