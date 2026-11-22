"""Binary classification confusion matrix, precision, and recall evaluation.

Extends '7.1 Data security key concepts.md'. Computes confusion matrix counts
(TP, FN, FP, TN), precision, and recall for binary classifier labels. Enforces
an explicit zero-denominator policy (returning 0.0 when denominators are zero).
Includes a worked input-to-output explanation and regression test execution.
"""

from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

LESSON_CITATION = "7.1 Data security key concepts.md"

# Normal canonical fixture
CANONICAL_Y_TRUE: tuple[int, ...] = (1, 1, 0, 0)
CANONICAL_Y_PRED: tuple[int, ...] = (1, 0, 1, 0)

# Boundary fixtures for zero-denominator policy verification
BOUNDARY_ZERO_PRED_TRUE: tuple[int, ...] = (1, 1, 0, 0)
BOUNDARY_ZERO_PRED_PRED: tuple[int, ...] = (0, 0, 0, 0)

BOUNDARY_ZERO_TRUE_TRUE: tuple[int, ...] = (0, 0)
BOUNDARY_ZERO_TRUE_PRED: tuple[int, ...] = (0, 1)

# Failure fixtures
FAILURE_MISMATCH_TRUE: tuple[int, ...] = (1, 0)
FAILURE_MISMATCH_PRED: tuple[int, ...] = (1,)

SCENARIO_EXPLANATIONS = {
    "normal": (
        f'Scenario: Canonical binary classification evaluation based on "{LESSON_CITATION}"; '
        "computes TP, FN, FP, TN, precision, and recall on balanced fixture."
    ),
    "boundary": (
        f'Scenario: Boundary checks for zero-denominator policy based on "{LESSON_CITATION}"; '
        "verifies precision=0.0 when no positive predictions and recall=0.0 when no positive true labels."
    ),
    "failure": (
        f'Scenario: Failure check based on "{LESSON_CITATION}"; '
        "rejects mismatched sequence lengths or non-binary labels."
    ),
}


@dataclass(frozen=True)
class ConfusionMetrics:
    """Immutable evaluation metrics container with explicit zero-denominator fallbacks."""

    tp: int
    fn: int
    fp: int
    tn: int

    @property
    def precision(self) -> float:
        """Precision = TP / (TP + FP); returns 0.0 if denominator is 0."""
        denom = self.tp + self.fp
        return (self.tp / denom) if denom > 0 else 0.0

    @property
    def recall(self) -> float:
        """Recall = TP / (TP + FN); returns 0.0 if denominator is 0."""
        denom = self.tp + self.fn
        return (self.tp / denom) if denom > 0 else 0.0


def validate_label_sequences(y_true: Sequence[int], y_pred: Sequence[int]) -> None:
    """Validate that label sequences are non-empty, equal length, and strictly binary 0/1 integers."""
    if not isinstance(y_true, Sequence) or not isinstance(y_pred, Sequence):
        raise TypeError("y_true and y_pred must be sequence types")
    if len(y_true) != len(y_pred):
        raise ValueError(
            f"Mismatched sequence lengths: len(y_true)={len(y_true)} != len(y_pred)={len(y_pred)}"
        )
    if len(y_true) == 0:
        raise ValueError("Label sequences must not be empty")

    for idx, (t, p) in enumerate(zip(y_true, y_pred)):
        if type(t) is not int or t not in (0, 1):
            raise ValueError(f"Invalid true label at index {idx}: {t!r}. Must be integer 0 or 1.")
        if type(p) is not int or p not in (0, 1):
            raise ValueError(f"Invalid predicted label at index {idx}: {p!r}. Must be integer 0 or 1.")


def compute_metrics(y_true: Sequence[int], y_pred: Sequence[int]) -> ConfusionMetrics:
    """Compute confusion matrix and metrics from true and predicted binary labels.

    Order contract: y_true first, y_pred second.
    Positive class is 1, negative class is 0.
    """
    validate_label_sequences(y_true, y_pred)

    tp = fn = fp = tn = 0
    for actual, pred in zip(y_true, y_pred):
        if actual == 1 and pred == 1:
            tp += 1
        elif actual == 1 and pred == 0:
            fn += 1
        elif actual == 0 and pred == 1:
            fp += 1
        elif actual == 0 and pred == 0:
            tn += 1

    return ConfusionMetrics(tp=tp, fn=fn, fp=fp, tn=tn)


def get_worked_explanation(
    y_true: Sequence[int] = CANONICAL_Y_TRUE,
    y_pred: Sequence[int] = CANONICAL_Y_PRED,
) -> str:
    """Generate a step-by-step worked input-to-output explanation."""
    validate_label_sequences(y_true, y_pred)
    lines = [
        "Worked Input-to-Output Explanation:",
        f"Input y_true: {list(y_true)}",
        f"Input y_pred: {list(y_pred)}",
        "Step-by-step element evaluation:",
    ]

    running_tp = running_fn = running_fp = running_tn = 0
    for idx, (t, p) in enumerate(zip(y_true, y_pred)):
        if t == 1 and p == 1:
            running_tp += 1
            category = "True Positive (TP)"
        elif t == 1 and p == 0:
            running_fn += 1
            category = "False Negative (FN)"
        elif t == 0 and p == 1:
            running_fp += 1
            category = "False Positive (FP)"
        else:
            running_tn += 1
            category = "True Negative (TN)"

        lines.append(
            f"  Index {idx}: actual={t}, predicted={p} -> {category} | Counts: TP={running_tp}, FN={running_fn}, FP={running_fp}, TN={running_tn}"
        )

    m = compute_metrics(y_true, y_pred)
    lines.extend([
        f"Final Confusion Matrix: TP={m.tp}, FN={m.fn}, FP={m.fp}, TN={m.tn}",
        f"Precision calculation: TP / (TP + FP) = {m.tp} / ({m.tp} + {m.fp}) = {m.precision:.3f}",
        f"Recall calculation:    TP / (TP + FN) = {m.tp} / ({m.tp} + {m.fn}) = {m.recall:.3f}",
        "Zero-denominator policy: If denominator is zero, metric defaults to 0.0.",
    ])
    return "\n".join(lines)


def run_scenario(scenario_name: str) -> tuple[int, str]:
    """Execute scenario by name ('normal', 'boundary', 'failure', 'explain')."""
    if scenario_name not in SCENARIO_EXPLANATIONS and scenario_name != "explain":
        return 1, f"Error: unknown scenario '{scenario_name}'"

    if scenario_name == "normal":
        m = compute_metrics(CANONICAL_Y_TRUE, CANONICAL_Y_PRED)
        output = (
            f"{SCENARIO_EXPLANATIONS['normal']}\n"
            f"y_true={list(CANONICAL_Y_TRUE)}, y_pred={list(CANONICAL_Y_PRED)}\n"
            f"Confusion matrix: TP={m.tp}, FN={m.fn}, FP={m.fp}, TN={m.tn}\n"
            f"precision={m.precision:.3f}, recall={m.recall:.3f}\n"
            "Zero-denominator policy: explicit 0.0 fallback when denominator is 0."
        )
        return 0, output

    if scenario_name == "boundary":
        m_zero_pred = compute_metrics(BOUNDARY_ZERO_PRED_TRUE, BOUNDARY_ZERO_PRED_PRED)
        m_zero_true = compute_metrics(BOUNDARY_ZERO_TRUE_TRUE, BOUNDARY_ZERO_TRUE_PRED)
        output = (
            f"{SCENARIO_EXPLANATIONS['boundary']}\n"
            f"No positive predictions (y_pred={list(BOUNDARY_ZERO_PRED_PRED)}): "
            f"TP={m_zero_pred.tp}, FN={m_zero_pred.fn}, FP={m_zero_pred.fp}, TN={m_zero_pred.tn} -> "
            f"precision={m_zero_pred.precision:.3f}, recall={m_zero_pred.recall:.3f}\n"
            f"No positive true labels (y_true={list(BOUNDARY_ZERO_TRUE_TRUE)}): "
            f"TP={m_zero_true.tp}, FN={m_zero_true.fn}, FP={m_zero_true.fp}, TN={m_zero_true.tn} -> "
            f"precision={m_zero_true.precision:.3f}, recall={m_zero_true.recall:.3f}"
        )
        return 0, output

    if scenario_name == "failure":
        try:
            compute_metrics(FAILURE_MISMATCH_TRUE, FAILURE_MISMATCH_PRED)
            return 0, f"{SCENARIO_EXPLANATIONS['failure']}\nUnexpected success for mismatched lengths"
        except ValueError as exc:
            return 1, f"{SCENARIO_EXPLANATIONS['failure']}\nError: {exc}"

    if scenario_name == "explain":
        explanation = get_worked_explanation(CANONICAL_Y_TRUE, CANONICAL_Y_PRED)
        return 0, explanation

    return 1, f"Unhandled scenario '{scenario_name}'"


def main(argv: Optional[List[str]] = None) -> int:
    """CLI entry point for running classification evaluation lab."""
    parser = argparse.ArgumentParser(
        description="Binary classification confusion matrix and precision/recall evaluator."
    )
    parser.add_argument(
        "--scenario",
        choices=["normal", "boundary", "failure", "explain"],
        default="normal",
        help="Scenario to run: normal (default), boundary, failure, or explain",
    )
    parser.add_argument(
        "--explain",
        action="store_true",
        help="Print detailed worked input-to-output explanation",
    )

    args = parser.parse_args(argv)

    scenario = "explain" if args.explain else args.scenario
    exit_code, output = run_scenario(scenario)
    if exit_code == 0:
        print(output)
    else:
        print(output, file=sys.stderr)
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
