# Binary Classification Metrics & Worked Explanation (R34-T026)

This applied lab extends **[7.1 Data security key concepts.md](../../7.1%20Data%20security%20key%20concepts.md)** by implementing a local, deterministic confusion matrix, precision, and recall evaluation tool for binary data classification.

## Overview

In data security and Data Loss Prevention (DLP), classifiers categorize documents as confidential (`1`) or non-confidential (`0`). Evaluating these systems requires exact metric accounting:
- **True Positive (TP)**: Sensitive data correctly flagged (`actual=1, predicted=1`).
- **False Negative (FN)**: Sensitive data mistakenly missed (`actual=1, predicted=0`).
- **False Positive (FP)**: Non-sensitive data mistakenly flagged (`actual=0, predicted=1`).
- **True Negative (TN)**: Non-sensitive data correctly cleared (`actual=0, predicted=0`).

### Explicit Zero-Denominator Policy
- **Precision**: $\frac{\text{TP}}{\text{TP} + \text{FP}}$ (evaluates to `0.0` when $\text{TP} + \text{FP} = 0$, e.g. no positive predictions).
- **Recall**: $\frac{\text{TP}}{\text{TP} + \text{FN}}$ (evaluates to `0.0` when $\text{TP} + \text{FN} = 0$, e.g. no positive true labels).

## Prerequisites and Invocation

- **Prerequisites**: Python 3 standard library. No external packages, cloud connections, GPUs, or model downloads required.
- **Invocation**:

From the repository root:

```bash
# Run canonical fixture evaluation
python3 ./applied-labs/r34-t026/example.py

# Print detailed worked input-to-output explanation
python3 ./applied-labs/r34-t026/example.py --explain

# Run boundary scenario (zero-denominator test cases)
python3 ./applied-labs/r34-t026/example.py --scenario boundary

# Run failure scenario (mismatched length rejection)
python3 ./applied-labs/r34-t026/example.py --scenario failure
```

## Worked Input-to-Output Explanation

Fixture:
- `y_true = [1, 1, 0, 0]`
- `y_pred = [1, 0, 1, 0]`

| Index | True Label (`y_true`) | Predicted Label (`y_pred`) | Classification Category | Running Counts |
| :---: | :---: | :---: | :---: | :---: |
| 0 | 1 | 1 | **True Positive (TP)** | TP=1, FN=0, FP=0, TN=0 |
| 1 | 1 | 0 | **False Negative (FN)** | TP=1, FN=1, FP=0, TN=0 |
| 2 | 0 | 1 | **False Positive (FP)** | TP=1, FN=1, FP=1, TN=0 |
| 3 | 0 | 0 | **True Negative (TN)** | TP=1, FN=1, FP=1, TN=1 |

### Metric Calculations
- **TP**: 1, **FN**: 1, **FP**: 1, **TN**: 1
- **Precision**: $\frac{\text{TP}}{\text{TP} + \text{FP}} = \frac{1}{1 + 1} = 0.500$
- **Recall**: $\frac{\text{TP}}{\text{TP} + \text{FN}} = \frac{1}{1 + 1} = 0.500$

## Exact Output Regression

```text
Scenario: Canonical binary classification evaluation based on "7.1 Data security key concepts.md"; computes TP, FN, FP, TN, precision, and recall on balanced fixture.
y_true=[1, 1, 0, 0], y_pred=[1, 0, 1, 0]
Confusion matrix: TP=1, FN=1, FP=1, TN=1
precision=0.500, recall=0.500
Zero-denominator policy: explicit 0.0 fallback when denominator is 0.
```

## Running the Automated Test Suite

Run unit tests via unittest discovery:

```bash
python3 -m unittest discover -s ./applied-labs/r34-t026 -p "test_*.py" -v
```

Expected result: 13 tests passing with zero failures.

## Scope and Limitations

This implementation is an educational Python simulation demonstrating arithmetic formulas and zero-division policies for binary confusion matrices. It evaluates synthetic in-memory fixtures. It does not train or evaluate real machine learning models, does not evaluate real data classification hardware, and makes no claims about production DLP software performance.
