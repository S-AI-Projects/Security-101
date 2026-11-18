"""Check fresh-process outputs, including documented error recovery."""

import argparse
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EXAMPLE = Path(__file__).with_name("example.py")

EXPECTED = {
    "normal": (
        0,
        "Scenario: normal (local fictional mock)\n"
        "Asset: Fictional employee mailbox credentials\n"
        "Threat: A phishing message tricks an employee into disclosing a password.\n"
        "Control: Verify unexpected sender requests and require multi-factor authentication for mailbox access.\n"
        "Residual risk: A stolen active session may still be misused before it is revoked.\n"
        "Missing fields: none\n"
        "Control review: matched (none)\n"
        "Rubric result: PASS\n",
        "",
    ),
    "boundary": (
        1,
        "Scenario: boundary (local fictional mock)\n"
        "Asset: MISSING\n"
        "Threat: Ransomware encrypts files in a shared project folder.\n"
        "Control: Keep tested offline backups to restore affected files.\n"
        "Residual risk: Recent changes may be lost between backups.\n"
        "Missing fields: asset\n"
        "Control review: matched (none)\n"
        "Rubric result: FAIL\n",
        "Error: missing required field(s): asset\n",
    ),
    "failure": (
        0,
        "Scenario: failure (local fictional mock)\n"
        "Asset: Fictional public appointment-booking service\n"
        "Threat: A DDoS attack makes the booking service unavailable.\n"
        "Control: Rotate employee passwords on a schedule.\n"
        "Residual risk: Password rotation does not reduce the incoming traffic that exhausts the service.\n"
        "Missing fields: none\n"
        "Control review: review (control category does not match the stated threat category)\n"
        "Rubric result: REVIEW\n",
        "",
    ),
    "recovery": (
        0,
        "Scenario: recovery (local fictional mock)\n"
        "Input 1: boundary (incomplete)\n"
        "Error: missing required field 'asset'\n"
        "Result 1: FAIL\n"
        "Input 2: normal (valid)\n"
        "Result 2: PASS\n"
        "Recovery: next valid input accepted\n",
        "",
    ),
}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--deliberate-failure",
        action="store_true",
        help="substitute a deliberately incorrect expected output",
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

    print("All scenario and recovery checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
