from collections.abc import Sequence
from dataclasses import dataclass


@dataclass(frozen=True)
class ConfusionMetrics:
    tp: int
    fn: int
    fp: int
    tn: int

    @property
    def precision(self) -> float:
        denominator = self.tp + self.fp
        return self.tp / denominator if denominator else 0.0

    @property
    def recall(self) -> float:
        denominator = self.tp + self.fn
        return self.tp / denominator if denominator else 0.0


def compute_metrics(
    y_true: Sequence[int], y_pred: Sequence[int]
) -> ConfusionMetrics:
    if len(y_true) != len(y_pred):
        raise ValueError("y_true and y_pred must have the same length")
    if not y_true:
        raise ValueError("label sequences must not be empty")

    counts = {"tp": 0, "fn": 0, "fp": 0, "tn": 0}
    for actual, predicted in zip(y_true, y_pred):
        if type(actual) is not int or actual not in (0, 1):
            raise ValueError("labels must be integers 0 or 1")
        if type(predicted) is not int or predicted not in (0, 1):
            raise ValueError("labels must be integers 0 or 1")

        if actual == 1 and predicted == 1:
            counts["tp"] += 1
        elif actual == 1:
            counts["fn"] += 1
        elif predicted == 1:
            counts["fp"] += 1
        else:
            counts["tn"] += 1

    return ConfusionMetrics(**counts)


def report_scenario(name: str, y_true: Sequence[int], y_pred: Sequence[int]) -> None:
    metrics = compute_metrics(y_true, y_pred)
    print(
        f"{name}: TP={metrics.tp}, FN={metrics.fn}, "
        f"FP={metrics.fp}, TN={metrics.tn}"
    )
    print(f"  precision={metrics.precision:.3f}, recall={metrics.recall:.3f}")


def main() -> None:
    y_true = [1, 1, 0, 0]
    scenarios = (
        ("balanced example", [1, 0, 1, 0]),
        ("recall-oriented predictions", [1, 1, 1, 0]),
        ("precision-oriented predictions", [1, 0, 0, 0]),
    )

    print("Local deterministic simulation; predictions are fixed fixtures.")
    for name, y_pred in scenarios:
        report_scenario(name, y_true, y_pred)
    print(
        "Trade-off: recall-oriented vs precision-oriented: "
        "recall 0.500 -> 1.000; precision 1.000 -> 0.667."
    )


if __name__ == "__main__":
    main()
