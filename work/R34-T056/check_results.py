"""Assertion checks for R34-T056 binary classification evaluation."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "applied-labs/r34-t056"))

from example import (
    compute_confusion_matrix,
    evaluate_binary_classification,
    evaluate_binary_classification_baseline,
    verify_refactoring_equivalence,
)


def main() -> int:
    y_true = [1, 1, 0, 0]
    y_pred = [1, 0, 1, 0]

    res = evaluate_binary_classification(y_true, y_pred)
    assert res["tp"] == 1
    assert res["fn"] == 1
    assert res["fp"] == 1
    assert res["tn"] == 1
    assert res["precision"] == 0.5
    assert res["recall"] == 0.5

    # Zero denominator
    zero_res = evaluate_binary_classification([1, 0], [0, 0])
    assert zero_res["precision"] == 0.0

    # Equivalence
    assert verify_refactoring_equivalence([([1, 1, 0, 0], [1, 0, 1, 0]), ([1, 0], [0, 0])])

    if "--deliberate-wrong-result" in sys.argv:
        assert res["precision"] == 1.0, "Deliberate wrong result check"

    print("All R34-T056 checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
