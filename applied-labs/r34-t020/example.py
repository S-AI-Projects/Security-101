"""A deterministic, local example of a shared-responsibility service adapter."""

import argparse
import sys
from collections.abc import Callable, Sequence
from typing import Protocol


VALID_SERVICE_MODELS = {"IaaS", "PaaS", "SaaS"}
VALID_OWNERS = {"customer", "provider", "shared"}

LOCAL_FIXTURE = (
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


class ResponsibilityAdapter(Protocol):
    """Callable interface for a source of responsibility records."""

    def __call__(self) -> object: ...


class AdapterError(RuntimeError):
    """Raised by an adapter when its source is unavailable."""


class ServiceAdapterError(RuntimeError):
    """Raised when the responsibility source cannot be read."""


class MatrixInputError(ValueError):
    """Raised when a responsibility record is malformed."""


class LocalServiceAdapter:
    """Return a fresh copy of the bundled mock records on each call."""

    def __init__(self, records: Sequence[dict[str, object]] = LOCAL_FIXTURE):
        self._records = tuple(dict(record) for record in records)

    def __call__(self) -> object:
        return [dict(record) for record in self._records]


def evaluate_responsibilities(records: object) -> list[dict[str, str]]:
    """Validate records and explicitly flag missing or invalid ownership."""
    if not isinstance(records, list):
        raise MatrixInputError("adapter result must be a list of records")

    matrix: list[dict[str, str]] = []
    for index, record in enumerate(records):
        if not isinstance(record, dict):
            raise MatrixInputError(f"record {index} must be a dictionary")

        task = record.get("task")
        if not isinstance(task, str) or not task.strip():
            raise MatrixInputError(f"record {index} must have a non-empty task")

        service_model = record.get("service_model")
        if not isinstance(service_model, str) or service_model not in VALID_SERVICE_MODELS:
            allowed = ", ".join(sorted(VALID_SERVICE_MODELS))
            raise MatrixInputError(
                f"record {index} has an invalid service_model; expected one of {allowed}"
            )

        if "responsible_party" not in record:
            responsible_party = "UNASSIGNED"
        else:
            owner = record["responsible_party"]
            responsible_party = (
                owner
                if isinstance(owner, str) and owner in VALID_OWNERS
                else "INVALID"
            )

        matrix.append(
            {
                "task": task.strip(),
                "service_model": service_model,
                "responsible_party": responsible_party,
            }
        )

    return matrix


def load_matrix(adapter: ResponsibilityAdapter) -> list[dict[str, str]]:
    """Call the source, then evaluate its result independently."""
    if not callable(adapter):
        raise TypeError("adapter must be callable")

    try:
        records = adapter()
    except AdapterError as error:
        raise ServiceAdapterError(f"responsibility adapter failed: {error}") from error

    return evaluate_responsibilities(records)


def format_matrix(matrix: Sequence[dict[str, str]]) -> str:
    lines = ["task | service_model | responsible_party"]
    lines.extend(
        f"{row['task']} | {row['service_model']} | {row['responsible_party']}"
        for row in matrix
    )
    return "\n".join(lines)


def _failure_adapter() -> object:
    raise AdapterError("mock source unavailable")


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--scenario",
        choices=("normal", "boundary", "failure"),
        default="normal",
        help="run the fixed fixture, an empty fixture, or a simulated adapter failure",
    )
    arguments = parser.parse_args(argv)

    if arguments.scenario == "boundary":
        adapter: Callable[[], object] = LocalServiceAdapter(records=())
    elif arguments.scenario == "failure":
        adapter = _failure_adapter
    else:
        adapter = LocalServiceAdapter()

    print(
        'Scenario: Illustrative ownership rows based on "1.6 Shared responsibility '
        'model.md"; these are mock records, not provider policy.',
        flush=True,
    )
    try:
        matrix = load_matrix(adapter)
    except (MatrixInputError, ServiceAdapterError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    print(format_matrix(matrix))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
