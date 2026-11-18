"""Compare fresh-process rubric results with independent expected output."""

import argparse
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EXAMPLE = Path(__file__).with_name("example.py")

EXPECTED = {
    "normal": (
        0,
        "\n".join(
            (
                "Scenario: normal (local fictional mock)",
                "Intermediate states: received -> normalized -> completeness -> control_review -> final",
                "Asset: Fictional customer-support training transcripts",
                "Threat: Personal information could be exposed from the training transcripts.",
                "Control: Remove direct identifiers and limit dataset access to approved staff because these steps reduce exposure of transcript data.",
                "Residual risk: Indirect identifiers may remain, and an authorized user could still misuse an accessible copy.",
                "Missing fields: none",
                "Control review: matched (none)",
                "Rubric result: PASS",
            )
        )
        + "\n",
        "",
    ),
    "boundary": (
        1,
        "\n".join(
            (
                "Scenario: boundary (local fictional mock)",
                "Intermediate states: received -> normalized -> completeness -> control_review -> final",
                "Asset: MISSING",
                "Threat: Personal information could be exposed from the training transcripts.",
                "Control: Remove direct identifiers and limit dataset access.",
                "Residual risk: Indirect identifiers may remain in the fictional dataset.",
                "Missing fields: asset",
                "Control review: matched (none)",
                "Rubric result: FAIL",
            )
        )
        + "\n",
        "",
    ),
    "failure": (
        0,
        "\n".join(
            (
                "Scenario: failure (local fictional mock)",
                "Intermediate states: received -> normalized -> completeness -> control_review -> final",
                "Asset: Fictional fraud-detection model and transaction review queue",
                "Threat: Crafted inputs could evade the model and hide fraudulent transactions.",
                "Control: Encrypt stored training data to reduce unauthorized access to that data.",
                "Residual risk: Evasion may still occur because encryption at rest does not assess the model's behavior on crafted inputs.",
                "Missing fields: none",
                "Control review: review (control category does not match the stated threat category)",
                "Rubric result: REVIEW",
            )
        )
        + "\n",
        "",
    ),
}


def run_scenario(scenario: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(EXAMPLE), "--scenario", scenario],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--deliberate-failure",
        action="store_true",
        help="substitute a deliberately wrong expected result",
    )
    arguments = parser.parse_args()

    for scenario, expected in EXPECTED.items():
        result = run_scenario(scenario)
        actual = (result.returncode, result.stdout, result.stderr)
        if arguments.deliberate_failure and scenario == "normal":
            expected = (0, "deliberately wrong result\n", "")
        assert actual == expected, (
            f"{scenario} result mismatch\n"
            f"expected: {expected!r}\n"
            f"actual:   {actual!r}"
        )
        print(f"{scenario}: matched explicit expected result")

    print("All scenario checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
