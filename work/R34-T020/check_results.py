"""Assertion-based evidence check; --deliberate-wrong-result must fail."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "applied-labs/r34-t020"))

from example import LocalServiceAdapter, evaluate_responsibilities, load_matrix


def main() -> int:
    matrix = load_matrix(LocalServiceAdapter())
    assert len(matrix) == 7
    assert {row["service_model"] for row in matrix} == {"IaaS", "PaaS", "SaaS"}
    assert [row["responsible_party"] for row in matrix] == [
        "customer",
        "provider",
        "customer",
        "provider",
        "customer",
        "provider",
        "shared",
    ]
    assert evaluate_responsibilities([]) == []
    assert evaluate_responsibilities(
        [{"task": "Missing", "service_model": "IaaS"}]
    )[0]["responsible_party"] == "UNASSIGNED"
    assert evaluate_responsibilities(
        [{"task": "Invalid", "service_model": "IaaS", "responsible_party": "other"}]
    )[0]["responsible_party"] == "INVALID"

    if "--deliberate-wrong-result" in sys.argv:
        assert matrix[0]["responsible_party"] == "provider"

    print("R34-T020 evidence assertions passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
