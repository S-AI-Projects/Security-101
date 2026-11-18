"""Verify the refactored CLI remains equivalent to the saved baseline."""

import argparse
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EXAMPLE = Path(__file__).with_name("example.py")
BASELINE_DIR = ROOT / "work" / "R34-T015"
EXPECTED_EXIT_CODES = {"normal": 0, "boundary": 1, "failure": 0}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--deliberate-failure",
        action="store_true",
        help="substitute a deliberately incorrect baseline expectation",
    )
    arguments = parser.parse_args()

    for scenario, expected_exit in EXPECTED_EXIT_CODES.items():
        baseline_output = (BASELINE_DIR / f"baseline-{scenario}-output.txt").read_text()
        if arguments.deliberate_failure and scenario == "normal":
            baseline_output = "deliberately wrong result\n"
        result = subprocess.run(
            [sys.executable, str(EXAMPLE), "--scenario", scenario],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
        )
        actual = (result.returncode, result.stdout, result.stderr)
        expected = (expected_exit, baseline_output, "")
        assert actual == expected, (
            f"{scenario} changed from the baseline\n"
            f"expected: {expected!r}\n"
            f"actual:   {actual!r}"
        )
        print(f"{scenario}: output and exit status match baseline")

    print("All baseline-equivalence checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
