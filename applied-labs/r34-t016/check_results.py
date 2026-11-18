"""Compare fresh-process CLI scenarios with explicit expected results."""

import argparse
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EXAMPLE = Path(__file__).with_name("example.py")

EXPECTED = {
    "normal": (
        0,
        "Scenario: normal (local fixture; no network traffic)\n"
        "Allowlist: 192.0.2.0/24\n"
        "Input address: 192.0.2.1\n"
        "Allowlisted: yes\n",
        "",
    ),
    "boundary": (
        0,
        "Scenario: boundary (local fixture; no network traffic)\n"
        "Allowlist: 192.0.2.0/24\n"
        "Input address: 198.51.100.1\n"
        "Allowlisted: no\n",
        "",
    ),
    "failure": (
        1,
        "Scenario: failure (local fixture; no network traffic)\n"
        "Allowlist: 192.0.2.0/24\n"
        "Input address: not-an-ip\n",
        "Error: invalid IP address 'not-an-ip'\n",
    ),
}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--deliberate-failure",
        action="store_true",
        help="use a deliberately incorrect expected result",
    )
    arguments = parser.parse_args()

    for scenario, expected in EXPECTED.items():
        result = subprocess.run(
            [sys.executable, str(EXAMPLE), "--scenario", scenario],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
        )
        actual = (result.returncode, result.stdout, result.stderr)
        if arguments.deliberate_failure and scenario == "normal":
            expected = (0, "deliberately wrong result\n", "")
        assert actual == expected, (
            f"{scenario} result mismatch\n"
            f"expected: {expected!r}\n"
            f"actual:   {actual!r}"
        )
        print(f"{scenario}: matched explicit expected result")

    print("All address checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
