"""Local IPv4 allowlist fixture for R34-T025.

This is a deterministic standard-library simulation. It performs no network
scanning and does not model a real firewall, cloud security group, or device.
"""

from __future__ import annotations

import argparse
import ipaddress
import sys
from typing import Iterable


LESSON_CITATION = "3.3 Network security capabilities.md"
DEFAULT_CIDR = "192.0.2.0/24"
CANONICAL_ADDRESS = "192.0.2.1"
OUTSIDE_ADDRESS = "198.51.100.1"
MALFORMED_ADDRESS = "192.0.2.not-an-ip"


class AddressAllowlist:
    """Named responsibility: parse an IPv4 CIDR and test address membership."""

    def __init__(self, cidr: str) -> None:
        try:
            self.network = ipaddress.IPv4Network(cidr, strict=True)
        except (ipaddress.AddressValueError, ipaddress.NetmaskValueError, ValueError) as exc:
            raise ValueError(f"Malformed CIDR: {cidr!r}") from exc

    def contains(self, address: str) -> bool:
        try:
            parsed = ipaddress.IPv4Address(address)
        except (ipaddress.AddressValueError, ValueError) as exc:
            raise ValueError(f"Malformed IPv4 address: {address!r}") from exc
        return parsed in self.network


def is_address_allowed(address: str, cidr: str = DEFAULT_CIDR) -> bool:
    """Return whether address is in cidr; reject malformed IPv4 input."""
    return AddressAllowlist(cidr).contains(address)


def baseline_address_allowed(address: str, cidr: str = DEFAULT_CIDR) -> bool:
    """Correct pre-refactor baseline preserving the public contract."""
    try:
        network = ipaddress.IPv4Network(cidr, strict=True)
    except (ipaddress.AddressValueError, ipaddress.NetmaskValueError, ValueError) as exc:
        raise ValueError(f"Malformed CIDR: {cidr!r}") from exc
    try:
        parsed = ipaddress.IPv4Address(address)
    except (ipaddress.AddressValueError, ValueError) as exc:
        raise ValueError(f"Malformed IPv4 address: {address!r}") from exc
    return parsed in network


def prove_fixture_equivalence(
    addresses: Iterable[str],
    cidr: str = DEFAULT_CIDR,
) -> tuple[dict[str, bool], bool]:
    """Compare baseline and extracted responsibility on the supplied fixture."""
    baseline = {address: baseline_address_allowed(address, cidr) for address in addresses}
    extracted = {address: is_address_allowed(address, cidr) for address in addresses}
    return extracted, baseline == extracted


def run_scenario(scenario: str) -> tuple[int, str]:
    if scenario == "normal":
        inside = is_address_allowed(CANONICAL_ADDRESS)
        outside = is_address_allowed(OUTSIDE_ADDRESS)
        output = (
            f'Scenario: allowlist membership based on "{LESSON_CITATION}".\n'
            f"CIDR={DEFAULT_CIDR}\n"
            f"{CANONICAL_ADDRESS} allowed={str(inside).lower()}\n"
            f"{OUTSIDE_ADDRESS} allowed={str(outside).lower()}"
        )
        return (0, output) if inside is True and outside is False else (1, "Unexpected result")

    if scenario == "boundary":
        results = [
            ("192.0.2.0", is_address_allowed("192.0.2.0")),
            ("192.0.2.255", is_address_allowed("192.0.2.255")),
            ("192.0.3.0", is_address_allowed("192.0.3.0")),
        ]
        output = (
            f'Scenario: boundary membership based on "{LESSON_CITATION}".\n'
            + "\n".join(f"{address} allowed={str(allowed).lower()}" for address, allowed in results)
        )
        expected = [("192.0.2.0", True), ("192.0.2.255", True), ("192.0.3.0", False)]
        return (0, output) if results == expected else (1, "Unexpected boundary result")

    if scenario == "failure":
        try:
            is_address_allowed(MALFORMED_ADDRESS)
            return 1, f'Scenario: failure based on "{LESSON_CITATION}".\nUnexpected success'
        except ValueError as exc:
            return 1, f'Scenario: failure based on "{LESSON_CITATION}".\nError: {exc}'

    if scenario == "explain":
        fixture = [CANONICAL_ADDRESS, OUTSIDE_ADDRESS]
        results, equivalent = prove_fixture_equivalence(fixture)
        output = (
            f"Worked fixture for {LESSON_CITATION}\n"
            f"CIDR={DEFAULT_CIDR}\n"
            f"{CANONICAL_ADDRESS} allowed={str(results[CANONICAL_ADDRESS]).lower()}\n"
            f"{OUTSIDE_ADDRESS} allowed={str(results[OUTSIDE_ADDRESS]).lower()}\n"
            f"baseline_extracted_equivalent={str(equivalent).lower()}"
        )
        return 0, output

    return 1, f"Unknown scenario: {scenario}"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Classify local IPv4 fixture addresses against an allowlisted CIDR."
    )
    parser.add_argument(
        "--scenario",
        choices=["normal", "boundary", "failure", "explain"],
        default="normal",
    )
    args = parser.parse_args(argv)
    exit_code, output = run_scenario(args.scenario)
    print(output, file=sys.stderr if exit_code != 0 else sys.stdout)
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
