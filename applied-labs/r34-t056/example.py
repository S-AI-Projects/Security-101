"""Binary Classification Evaluation and Refactoring Equivalence (R34-T056).

Extends 7.1 Data security key concepts.
Computes confusion matrix (TP, FN, FP, TN), precision, and recall for binary data classifiers.
Enforces an explicit zero-denominator policy (returns 0.0 when denominator is zero).
Extracts confusion matrix calculation as a distinct responsibility and proves before/after equivalence.
"""

from __future__ import annotations

import argparse
import sys
from typing import Any, Dict, List, NamedTuple, Sequence, Tuple


class ConfusionMatrix(NamedTuple):
    tp: int
    fn: int
    fp: int
    tn: int


class ClassificationMetrics(NamedTuple):
    confusion_matrix: ConfusionMatrix
    precision: float
    recall: float


def evaluate_binary_classification_baseline(
    y_true: Sequence[int], y_pred: Sequence[int]
) -> Dict[str, Any]:
    """Baseline monolithic implementation calculating confusion matrix, precision, and recall."""
    if len(y_true) != len(y_pred):
        raise ValueError(f"Length mismatch: y_true ({len(y_true)}) != y_pred ({len(y_pred)})")

    tp = fn = fp = tn = 0
    for yt, yp in zip(y_true, y_pred):
        if yt not in (0, 1) or yp not in (0, 1):
            raise ValueError(f"Labels must be 0 or 1, got yt={yt}, yp={yp}")
        if yt == 1 and yp == 1:
            tp += 1
        elif yt == 1 and yp == 0:
            fn += 1
        elif yt == 0 and yp == 1:
            fp += 1
        elif yt == 0 and yp == 0:
            tn += 1

    # Zero-denominator policy: return 0.0 if denominator is zero
    precision = float(tp) / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = float(tp) / (tp + fn) if (tp + fn) > 0 else 0.0

    return {
        "tp": tp,
        "fn": fn,
        "fp": fp,
        "tn": tn,
        "precision": round(precision, 4),
        "recall": round(recall, 4),
    }


def compute_confusion_matrix(
    y_true: Sequence[int], y_pred: Sequence[int]
) -> ConfusionMatrix:
    """Extracted named responsibility: computes only the counts (TP, FN, FP, TN)."""
    if len(y_true) != len(y_pred):
        raise ValueError(f"Length mismatch: y_true ({len(y_true)}) != y_pred ({len(y_pred)})")

    tp = fn = fp = tn = 0
    for yt, yp in zip(y_true, y_pred):
        if yt not in (0, 1) or yp not in (0, 1):
            raise ValueError(f"Labels must be 0 or 1, got yt={yt}, yp={yp}")
        if yt == 1 and yp == 1:
            tp += 1
        elif yt == 1 and yp == 0:
            fn += 1
        elif yt == 0 and yp == 1:
            fp += 1
        elif yt == 0 and yp == 0:
            tn += 1

    return ConfusionMatrix(tp=tp, fn=fn, fp=fp, tn=tn)


def compute_metrics_from_matrix(cm: ConfusionMatrix) -> Dict[str, Any]:
    """Extracted responsibility: computes precision and recall from confusion matrix counts."""
    # Zero-denominator policy: return 0.0 when denominator is 0
    prec_denom = cm.tp + cm.fp
    rec_denom = cm.tp + cm.fn
    precision = float(cm.tp) / prec_denom if prec_denom > 0 else 0.0
    recall = float(cm.tp) / rec_denom if rec_denom > 0 else 0.0

    return {
        "tp": cm.tp,
        "fn": cm.fn,
        "fp": cm.fp,
        "tn": cm.tn,
        "precision": round(precision, 4),
        "recall": round(recall, 4),
    }


def evaluate_binary_classification(
    y_true: Sequence[int], y_pred: Sequence[int]
) -> Dict[str, Any]:
    """Refactored pipeline composing extracted responsibilities."""
    cm = compute_confusion_matrix(y_true, y_pred)
    return compute_metrics_from_matrix(cm)


def verify_refactoring_equivalence(fixtures: List[Tuple[Sequence[int], Sequence[int]]]) -> bool:
    """Proves byte-for-byte equivalence between baseline and refactored implementation."""
    for yt, yp in fixtures:
        baseline_res = evaluate_binary_classification_baseline(yt, yp)
        refactored_res = evaluate_binary_classification(yt, yp)
        if baseline_res != refactored_res:
            return False
    return True


def run_demonstration(scenario: str) -> int:
    print(f"Scenario: {scenario}")

    if scenario == "normal":
        # Standard lesson fixture
        y_true = [1, 1, 0, 0]
        y_pred = [1, 0, 1, 0]
        res = evaluate_binary_classification(y_true, y_pred)
        print(f"y_true: {y_true}")
        print(f"y_pred: {y_pred}")
        print(f"Confusion Matrix: TP={res['tp']}, FN={res['fn']}, FP={res['fp']}, TN={res['tn']}")
        print(f"Precision: {res['precision']}, Recall: {res['recall']}")

        assert res["tp"] == 1
        assert res["fn"] == 1
        assert res["fp"] == 1
        assert res["tn"] == 1
        assert res["precision"] == 0.5
        assert res["recall"] == 0.5

        # Refactoring equivalence check
        fixtures = [
            ([1, 1, 0, 0], [1, 0, 1, 0]),
            ([1, 0], [0, 0]),
            ([1, 1], [1, 1]),
            ([0, 0], [0, 0]),
        ]
        assert verify_refactoring_equivalence(fixtures), "Refactoring equivalence failed!"
        print("Refactoring equivalence between baseline and modular design verified.")
        return 0

    elif scenario == "boundary":
        # Zero-denominator boundary fixture: No positive predictions (precision denom=0)
        y_true = [1, 0]
        y_pred = [0, 0]
        res = evaluate_binary_classification(y_true, y_pred)
        print(f"Zero-prediction boundary: y_true={y_true}, y_pred={y_pred}")
        print(f"Result: TP={res['tp']}, FP={res['fp']}, Precision={res['precision']}")
        assert res["tp"] == 0
        assert res["fp"] == 0
        assert res["precision"] == 0.0, "Zero-denominator policy failed!"
        return 0

    elif scenario == "failure":
        # Failure case: Length mismatch raises ValueError and exits 1
        print("Failure simulation check: Length mismatch...", file=sys.stderr)
        try:
            evaluate_binary_classification([1, 0], [1])
            return 0
        except ValueError as err:
            print(f"Expected failure caught: {err}", file=sys.stderr)
            return 1

    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Binary Classification Evaluation")
    parser.add_argument(
        "--scenario",
        choices=["normal", "boundary", "failure"],
        default="normal",
        help="Scenario mode to execute",
    )
    args = parser.parse_args()
    return run_demonstration(args.scenario)


if __name__ == "__main__":
    sys.exit(main())
