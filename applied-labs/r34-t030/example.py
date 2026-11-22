"""A teaching responsibility matrix example for the shared responsibility model.

This module implements a deterministic, local teaching responsibility matrix
illustrating cloud security ownership across IaaS, PaaS, and SaaS based on
'1.6 Shared responsibility model.md'. It explicitly flags missing or invalid
ownership rather than assuming the cloud service provider handles it.
"""

from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence
from typing import Any, Dict, List, Optional, Tuple

VALID_SERVICE_MODELS = ("IaaS", "PaaS", "SaaS")
VALID_RESPONSIBLE_PARTIES = ("customer", "provider", "shared")

LESSON_CITATION = "1.6 Shared responsibility model.md"

# Normal fixture: every task has explicit customer/provider/shared ownership
NORMAL_FIXTURE: tuple[dict[str, str], ...] = (
    {
        "task": "Patch guest operating system",
        "service_model": "IaaS",
        "responsible_party": "customer",
    },
    {
        "task": "Protect physical host",
        "service_model": "IaaS",
        "responsible_party": "provider",
    },
    {
        "task": "Secure application code",
        "service_model": "PaaS",
        "responsible_party": "customer",
    },
    {
        "task": "Patch managed runtime",
        "service_model": "PaaS",
        "responsible_party": "provider",
    },
    {
        "task": "Configure user access",
        "service_model": "SaaS",
        "responsible_party": "customer",
    },
    {
        "task": "Protect hosted application",
        "service_model": "SaaS",
        "responsible_party": "provider",
    },
    {
        "task": "Review data handling",
        "service_model": "PaaS",
        "responsible_party": "shared",
    },
)

# Boundary fixture: unassigned ownership tasks to test flagging policy
BOUNDARY_FIXTURE: tuple[dict[str, Any], ...] = (
    {
        "task": "Configure network security groups",
        "service_model": "IaaS",
    },
    {
        "task": "Define API rate limits",
        "service_model": "PaaS",
        "responsible_party": "",
    },
    {
        "task": "Enforce MFA on user accounts",
        "service_model": "SaaS",
        "responsible_party": None,
    },
)

# Failure fixture: malformed or invalid service model records
FAILURE_FIXTURE: tuple[dict[str, Any], ...] = (
    {
        "task": "Maintain server hardware",
        "service_model": "OnPremise",
        "responsible_party": "customer",
    },
)

SCENARIO_EXPLANATIONS = {
    "normal": (
        f'Scenario: Illustrative teaching responsibility matrix based on "{LESSON_CITATION}"; '
        "these are educational mock records, not real provider policy."
    ),
    "boundary": (
        f'Scenario: Boundary check for unassigned ownership based on "{LESSON_CITATION}"; '
        "flags missing ownership rather than assuming provider coverage."
    ),
    "failure": (
        f'Scenario: Failure check based on "{LESSON_CITATION}"; '
        "rejects malformed records or invalid service models."
    ),
}

APPLIED_QUESTIONS: dict[str, dict[str, str]] = {
    "question_1": {
        "title": "Predict an output",
        "question": (
            "What is the evaluated responsible party for the task "
            "'Patch guest operating system' under the 'IaaS' service model?"
        ),
        "expected_answer": "customer",
        "rationale": (
            "Under Infrastructure as a Service (IaaS), the cloud provider manages the physical "
            "hosts and virtualization layer, but the customer retains full responsibility for the "
            "guest operating system, its security configuration, and routine patch management, as "
            f'explained in "{LESSON_CITATION}".'
        ),
        "executable_check": "test_question_1_predict_output",
    },
    "question_2": {
        "title": "Diagnose a failure",
        "question": (
            "Why does evaluating {'task': 'Enforce MFA on user accounts', 'service_model': 'SaaS'} "
            "fail to assign provider ownership, and how is it evaluated?"
        ),
        "expected_answer": "UNASSIGNED",
        "rationale": (
            "In Software as a Service (SaaS), user credential management and access controls "
            "remain the customer's duty. When responsible_party is omitted, our policy flags the "
            "ownership as UNASSIGNED rather than dangerously assuming the cloud provider covers it."
        ),
        "executable_check": "test_question_2_diagnose_failure",
    },
    "question_3": {
        "title": "Choose a boundary policy",
        "question": (
            "When a workload security task has no assigned responsible party, what boundary policy "
            "must be applied: default-to-provider, default-to-customer, or flag as UNASSIGNED?"
        ),
        "expected_answer": "UNASSIGNED",
        "rationale": (
            "Defaulting to provider leads to false assumptions of protection ('trust without verify'), "
            "causing severe security gaps. Defaulting to customer can misclassify physical data center "
            "controls. The safe boundary policy is to flag unassigned tasks as UNASSIGNED to enforce "
            f'explicit review and audit per "{LESSON_CITATION}".'
        ),
        "executable_check": "test_question_3_choose_boundary_policy",
    },
}


def evaluate_task_responsibility(entry: dict[str, Any]) -> dict[str, str]:
    """Evaluate a single responsibility matrix entry.

    Validates task name and cloud service model, and evaluates the responsible
    party. If responsible_party is missing, None, or empty, it is flagged as
    'UNASSIGNED' rather than defaulting to provider. If the responsible_party
    is invalid, it is flagged as 'INVALID'.
    """
    if not isinstance(entry, dict):
        raise TypeError(f"Matrix entry must be a dictionary, got {type(entry).__name__}")

    raw_task = entry.get("task")
    if not isinstance(raw_task, str) or not raw_task.strip():
        raise ValueError("Task must be a non-empty string")
    task = raw_task.strip()

    raw_model = entry.get("service_model")
    if not isinstance(raw_model, str) or raw_model.strip() not in VALID_SERVICE_MODELS:
        allowed = ", ".join(VALID_SERVICE_MODELS)
        raise ValueError(f"Invalid service model '{raw_model}' for task '{task}'. Allowed models: {allowed}")
    service_model = raw_model.strip()

    raw_party = entry.get("responsible_party")
    if raw_party is None or (isinstance(raw_party, str) and not raw_party.strip()):
        responsible_party = "UNASSIGNED"
        status = "FLAGGED_UNASSIGNED"
    elif isinstance(raw_party, str) and raw_party.strip() in VALID_RESPONSIBLE_PARTIES:
        responsible_party = raw_party.strip()
        status = "ASSIGNED"
    else:
        responsible_party = "INVALID"
        status = "FLAGGED_INVALID"

    return {
        "task": task,
        "service_model": service_model,
        "responsible_party": responsible_party,
        "status": status,
    }


def evaluate_matrix(entries: Sequence[dict[str, Any]]) -> list[dict[str, str]]:
    """Evaluate a sequence of responsibility entries."""
    return [evaluate_task_responsibility(e) for e in entries]


def format_matrix(evaluated_entries: list[dict[str, str]]) -> str:
    """Format evaluated matrix records into a pipe-delimited table."""
    lines = ["task | service_model | responsible_party"]
    for row in evaluated_entries:
        lines.append(f"{row['task']} | {row['service_model']} | {row['responsible_party']}")
    return "\n".join(lines)


def run_scenario(scenario_name: str) -> tuple[int, str]:
    """Execute a scenario by name ('normal', 'boundary', 'failure').

    Returns a tuple of (exit_code, output_text).
    """
    if scenario_name not in SCENARIO_EXPLANATIONS:
        return 1, f"Error: unknown scenario '{scenario_name}'"

    explanation = SCENARIO_EXPLANATIONS[scenario_name]

    if scenario_name == "normal":
        evaluated = evaluate_matrix(NORMAL_FIXTURE)
        output = f"{explanation}\n{format_matrix(evaluated)}"
        return 0, output

    if scenario_name == "boundary":
        evaluated = evaluate_matrix(BOUNDARY_FIXTURE)
        output = f"{explanation}\n{format_matrix(evaluated)}"
        return 0, output

    if scenario_name == "failure":
        try:
            evaluate_matrix(FAILURE_FIXTURE)
            return 0, f"{explanation}\nUnexpected success for failure fixture"
        except ValueError as exc:
            return 1, f"{explanation}\nError: {exc}"

    return 1, f"Unhandled scenario '{scenario_name}'"


def main(argv: Optional[List[str]] = None) -> int:
    """CLI entry point for running the responsibility matrix lab."""
    parser = argparse.ArgumentParser(
        description="Offline teaching responsibility matrix for the shared responsibility model."
    )
    parser.add_argument(
        "--scenario",
        choices=["normal", "boundary", "failure"],
        default="normal",
        help="Scenario to run: normal (default), boundary, or failure",
    )
    parser.add_argument(
        "--questions",
        action="store_true",
        help="Print the three applied questions, answers, and rationales.",
    )

    args = parser.parse_args(argv)

    if args.questions:
        print("Applied Questions on 1.6 Shared Responsibility Matrix:")
        print("=" * 60)
        for key, item in APPLIED_QUESTIONS.items():
            print(f"[{item['title']}]")
            print(f"Q: {item['question']}")
            print(f"A: {item['expected_answer']}")
            print(f"Rationale: {item['rationale']}")
            print(f"Executable Check: {item['executable_check']}")
            print("-" * 60)
        return 0

    exit_code, output = run_scenario(args.scenario)
    if exit_code == 0:
        print(output)
    else:
        print(output, file=sys.stderr)
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
