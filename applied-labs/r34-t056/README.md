# Binary Classification Evaluation and Refactoring Equivalence (R34-T056)

This applied lab extends **7.1 Data security key concepts** by evaluating binary classification metrics (confusion matrix, precision, and recall) for data security classifiers and proving refactoring equivalence.

## Overview

In data security (e.g. data classification, DLP scanning, secret detection), automated classifiers tag assets or records as sensitive (1) or non-sensitive (0). Evaluating classifier effectiveness requires computing:
- **True Positives (TP)**: Sensitive data correctly flagged.
- **False Negatives (FN)**: Sensitive data missed (confidentiality risk).
- **False Positives (FP)**: Non-sensitive data incorrectly flagged (operational overhead).
- **True Negatives (TN)**: Non-sensitive data correctly ignored.
- **Precision**: `TP / (TP + FP)`
- **Recall**: `TP / (TP + FN)`

### Zero-Denominator Policy

When no positive predictions are made (`TP + FP == 0`), precision is explicitly defined as `0.0` (rather than causing division-by-zero or returning undefined NaN). Similarly, when no true positive samples exist (`TP + FN == 0`), recall is defined as `0.0`.

### Refactoring and Separation of Responsibilities

The codebase demonstrates software modularity by:
1. Providing a correct monolithic baseline: `evaluate_binary_classification_baseline`.
2. Extracting the calculation of counts as a single named responsibility: `compute_confusion_matrix`.
3. Calculating precision and recall in `compute_metrics_from_matrix`.
4. Composing them in `evaluate_binary_classification`.
5. Proving before-and-after byte-for-byte equivalence across test fixtures.

## Invocation

```bash
python3 ./applied-labs/r34-t056/example.py
python3 ./applied-labs/r34-t056/example.py --scenario boundary
python3 ./applied-labs/r34-t056/example.py --scenario failure
```

## Running Tests

```bash
python3 -m unittest discover -s ./applied-labs/r34-t056 -p "test_*.py"
```

## Scope and Limitations

This script performs exact mathematical evaluation of binary labels using Python standard library structures. It does not train ML models or download external weights.
