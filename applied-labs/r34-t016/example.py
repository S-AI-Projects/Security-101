"""Classify local example IP addresses against one allowlisted CIDR."""

import argparse
import ipaddress
import sys
from collections.abc import Sequence


ALLOWLIST_CIDR = "192.0.2.0/24"
ALLOWLIST_NETWORK = ipaddress.ip_network(ALLOWLIST_CIDR, strict=True)
SCENARIO_ADDRESSES = {
    "normal": "192.0.2.1",
    "boundary": "198.51.100.1",
    "failure": "not-an-ip",
}


def is_allowlisted(address: str) -> bool:
    """Return whether a valid IP address belongs to the example network."""
    try:
        parsed_address = ipaddress.ip_address(address)
    except ValueError as error:
        raise ValueError(f"invalid IP address {address!r}") from error
    return parsed_address in ALLOWLIST_NETWORK


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--scenario",
        choices=tuple(SCENARIO_ADDRESSES),
        default="normal",
        help="check the in-network, out-of-network, or malformed local example",
    )
    arguments = parser.parse_args(argv)
    address = SCENARIO_ADDRESSES[arguments.scenario]

    print(f"Scenario: {arguments.scenario} (local fixture; no network traffic)")
    print(f"Allowlist: {ALLOWLIST_CIDR}")
    print(f"Input address: {address}", flush=True)
    try:
        allowlisted = is_allowlisted(address)
    except ValueError as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    print(f"Allowlisted: {'yes' if allowlisted else 'no'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
