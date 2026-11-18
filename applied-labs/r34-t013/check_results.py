"""Compare fresh-process example output with explicit expected results."""

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
                "Scenario: normal (local mock)",
                "Client capabilities: ['resources', 'tools']",
                "Server capabilities: ['prompts', 'tools']",
                "Negotiated capabilities: ['tools']",
                "Result: tools dispatched",
            )
        )
        + "\n",
        "",
    ),
    "boundary": (
        1,
        "\n".join(
            (
                "Scenario: boundary (local mock)",
                "Client capabilities: ['resources']",
                "Server capabilities: ['prompts', 'tools']",
                "Negotiated capabilities: []",
                "Rejected: capability 'tools' was not negotiated",
                "Handler invoked: False",
            )
        )
        + "\n",
        "",
    ),
    "failure": (
        1,
        "\n".join(
            (
                "Scenario: failure (local mock)",
                "Client capabilities: ['resources', 'tools']",
                "Server capabilities: ['prompts', 'tools']",
                "Negotiated capabilities: ['tools']",
                "Rejected: capability 'resources' was not negotiated",
                "Handler invoked: False",
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
        help="use a deliberately incorrect expectation to verify assertion failure",
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
