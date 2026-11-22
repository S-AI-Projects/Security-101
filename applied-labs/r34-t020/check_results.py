"""Run R34-T020 scenarios and save machine-readable verification evidence."""

import json
import platform
import subprocess
import sys
from pathlib import Path


LAB_DIR = Path(__file__).resolve().parent
REPO_ROOT = LAB_DIR.parents[1]
EVIDENCE_DIR = REPO_ROOT / "work" / "R34-T020"


def run_scenario(name: str) -> dict[str, object]:
    completed = subprocess.run(
        [sys.executable, "example.py", "--scenario", name],
        cwd=LAB_DIR,
        text=True,
        capture_output=True,
        check=False,
    )
    return {
        "scenario": name,
        "command": f"{sys.executable} example.py --scenario {name}",
        "exit_code": completed.returncode,
        "stdout": completed.stdout,
        "stderr": completed.stderr,
    }


def main() -> int:
    EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)
    scenarios = [run_scenario(name) for name in ("normal", "boundary", "failure")]
    expected = {
        "normal": {
            "exit_code": 0,
            "owner_rows": 7,
            "owners": ["customer", "provider", "shared"],
        },
        "boundary": {
            "exit_code": 0,
            "output": "task | service_model | responsible_party",
        },
        "failure": {
            "exit_code": 1,
            "stderr": "Error: responsibility adapter failed: mock source unavailable",
        },
    }
    for scenario in scenarios:
        name = str(scenario["scenario"])
        scenario["expected"] = expected[name]
        scenario["matches_expected"] = (
            scenario["exit_code"] == expected[name]["exit_code"]
            and (
                name != "normal"
                or all(owner in str(scenario["stdout"]) for owner in expected[name]["owners"])
            )
            and (
                name != "boundary"
                or expected[name]["output"] in str(scenario["stdout"])
            )
            and (
                name != "failure"
                or expected[name]["stderr"] in str(scenario["stderr"])
            )
        )

    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "unittest",
            "discover",
            "-s",
            str(LAB_DIR),
            "-p",
            "test_*.py",
        ],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )

    evidence = {
        "scenarios": scenarios,
        "unit_test": {
            "command": (
                "python3 -m unittest discover -s ./applied-labs/r34-t020 "
                '-p "test_*.py"'
            ),
            "exit_code": completed.returncode,
            "stdout": completed.stdout,
            "stderr": completed.stderr,
        },
        "tool_versions": {
            "python": platform.python_version(),
            "python_executable": sys.executable,
            "platform": platform.platform(),
        },
    }
    (EVIDENCE_DIR / "check-results.json").write_text(
        json.dumps(evidence, indent=2) + "\n",
        encoding="utf-8",
    )
    print(completed.stdout, end="")
    print(completed.stderr, end="", file=sys.stderr)
    return completed.returncode


if __name__ == "__main__":
    raise SystemExit(main())
