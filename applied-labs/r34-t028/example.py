"""Offline network range classification and error recovery example.

Extends '3.3 Network security capabilities.md'. Uses Python's standard ipaddress
module to classify sample IP addresses against an allowlisted CIDR range without
active scanning or packet transmission. Demonstrates error handling on invalid
and missing inputs, followed by recovery on subsequent valid inputs.
"""

from __future__ import annotations

import argparse
import ipaddress
import sys
from collections.abc import Sequence
from typing import Any, Dict, List, Optional, Tuple

LESSON_CITATION = "3.3 Network security capabilities.md"
DEFAULT_ALLOWLIST_CIDR = "192.0.2.0/24"

NORMAL_SAMPLES: tuple[Optional[str], ...] = (
    "192.0.2.1",
    "198.51.100.1",
    "invalid-ip-string",
    "",
    "192.0.2.42",
)

BOUNDARY_SAMPLES: tuple[str, ...] = (
    "192.0.2.0",    # Network address
    "192.0.2.255",  # Broadcast address
    "192.0.3.1",    # Adjacent subnet
)

FAILURE_CIDR_FIXTURE = "192.0.2.0/99"

SCENARIO_EXPLANATIONS = {
    "normal": (
        f'Scenario: Illustrative network range classification based on "{LESSON_CITATION}"; '
        "educational mock CIDR checks, no network scanning."
    ),
    "boundary": (
        f'Scenario: Boundary checks for CIDR network classification based on "{LESSON_CITATION}"; '
        "evaluates network boundaries and adjacent ranges."
    ),
    "failure": (
        f'Scenario: Failure check based on "{LESSON_CITATION}"; '
        "rejects invalid or malformed network CIDR definitions."
    ),
}


def classify_address(
    ip_str: Optional[str],
    network_cidr: str = DEFAULT_ALLOWLIST_CIDR,
) -> dict[str, Any]:
    """Classify a single IP address against an allowlisted CIDR network range.

    Returns a structured dictionary with:
    - input: original input representation
    - status: 'ALLOW', 'DENY', or 'ERROR'
    - is_member: bool (True for in-range, False for out-of-range, None on error)
    - error_type: 'MISSING_DATA' | 'MALFORMED_IP' | None
    - message: descriptive result explanation
    """
    try:
        network = ipaddress.ip_network(network_cidr, strict=False)
    except ValueError as exc:
        raise ValueError(f"Invalid network CIDR '{network_cidr}': {exc}") from exc

    if ip_str is None or not str(ip_str).strip():
        return {
            "input": ip_str,
            "status": "ERROR",
            "is_member": None,
            "error_type": "MISSING_DATA",
            "message": "Missing data: IP address string cannot be empty or None.",
        }

    cleaned = str(ip_str).strip()
    try:
        ip_obj = ipaddress.ip_address(cleaned)
    except ValueError as exc:
        return {
            "input": cleaned,
            "status": "ERROR",
            "is_member": None,
            "error_type": "MALFORMED_IP",
            "message": f"Malformed input: '{cleaned}' is not a valid IPv4 or IPv6 address ({exc}).",
        }

    # IPv4 vs IPv6 version mismatch check
    if ip_obj.version != network.version:
        return {
            "input": cleaned,
            "status": "DENY",
            "is_member": False,
            "error_type": None,
            "message": f"IP version mismatch (IPv{ip_obj.version} vs IPv{network.version}); external to allowlist.",
        }

    if ip_obj in network:
        return {
            "input": cleaned,
            "status": "ALLOW",
            "is_member": True,
            "error_type": None,
            "message": f"Address {cleaned} belongs to allowlisted network {network_cidr}.",
        }
    else:
        return {
            "input": cleaned,
            "status": "DENY",
            "is_member": False,
            "error_type": None,
            "message": f"Address {cleaned} does not belong to allowlisted network {network_cidr}.",
        }


def classify_sequence(
    ip_list: Sequence[Optional[str]],
    network_cidr: str = DEFAULT_ALLOWLIST_CIDR,
) -> list[dict[str, Any]]:
    """Process a sequence of IP addresses, handling errors and recovering on next valid input."""
    return [classify_address(ip, network_cidr=network_cidr) for ip in ip_list]


def format_classification_output(results: Sequence[dict[str, Any]], network_cidr: str) -> str:
    """Format classification results into human-readable lines."""
    lines = [f"Allowlisted Network: {network_cidr}"]
    for r in results:
        raw = repr(r["input"]) if r["input"] in (None, "") else r["input"]
        if r["status"] == "ALLOW":
            lines.append(f"[ALLOW] IP: {raw} -> Belongs to {network_cidr}")
        elif r["status"] == "DENY":
            lines.append(f"[DENY]  IP: {raw} -> Outside {network_cidr}")
        else:
            lines.append(f"[ERROR] IP: {raw} -> {r['error_type']}: {r['message']}")
    return "\n".join(lines)


def run_scenario(scenario_name: str) -> tuple[int, str]:
    """Execute scenario by name ('normal', 'boundary', 'failure', 'recovery')."""
    if scenario_name not in SCENARIO_EXPLANATIONS and scenario_name != "recovery":
        return 1, f"Error: unknown scenario '{scenario_name}'"

    explanation = SCENARIO_EXPLANATIONS.get(
        scenario_name,
        f'Scenario: Focus on recovery based on "{LESSON_CITATION}"; proves parser state resilience.',
    )

    if scenario_name == "normal":
        results = classify_sequence(NORMAL_SAMPLES, DEFAULT_ALLOWLIST_CIDR)
        output = (
            f"{explanation}\n"
            f"{format_classification_output(results, DEFAULT_ALLOWLIST_CIDR)}\n"
            "Recovery: Following malformed/missing entries, subsequent valid address was processed successfully."
        )
        return 0, output

    if scenario_name == "boundary":
        results = classify_sequence(BOUNDARY_SAMPLES, DEFAULT_ALLOWLIST_CIDR)
        output = f"{explanation}\n{format_classification_output(results, DEFAULT_ALLOWLIST_CIDR)}"
        return 0, output

    if scenario_name == "failure":
        try:
            classify_address("192.0.2.1", network_cidr=FAILURE_CIDR_FIXTURE)
            return 0, f"{explanation}\nUnexpected success for invalid network CIDR"
        except ValueError as exc:
            return 1, f"{explanation}\nError: {exc}"

    if scenario_name == "recovery":
        seq = ["invalid-ip", "192.0.2.1"]
        res = classify_sequence(seq, DEFAULT_ALLOWLIST_CIDR)
        output = (
            f"{explanation}\n"
            f"Step 1 (Invalid): {res[0]['status']} - {res[0]['error_type']}\n"
            f"Step 2 (Recovery on next valid): {res[1]['status']} (Member: {res[1]['is_member']})"
        )
        return 0, output

    return 1, f"Unhandled scenario '{scenario_name}'"


def main(argv: Optional[List[str]] = None) -> int:
    """CLI entry point for running the network classification lab."""
    parser = argparse.ArgumentParser(
        description="Offline network range classification and error recovery example."
    )
    parser.add_argument(
        "--scenario",
        choices=["normal", "boundary", "failure", "recovery"],
        default="normal",
        help="Scenario to run: normal (default), boundary, failure, or recovery",
    )
    parser.add_argument(
        "--cidr",
        default=DEFAULT_ALLOWLIST_CIDR,
        help=f"Allowlisted CIDR network range (default: {DEFAULT_ALLOWLIST_CIDR})",
    )
    parser.add_argument(
        "--ip",
        help="Evaluate a specific single IP address against the CIDR",
    )

    args = parser.parse_args(argv)

    if args.ip is not None:
        result = classify_address(args.ip, network_cidr=args.cidr)
        print(f"Status: {result['status']}")
        print(f"Member: {result['is_member']}")
        print(f"Message: {result['message']}")
        return 0

    exit_code, output = run_scenario(args.scenario)
    if exit_code == 0:
        print(output)
    else:
        print(output, file=sys.stderr)
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
