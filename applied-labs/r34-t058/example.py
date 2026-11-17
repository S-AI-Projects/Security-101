"""Network Range Classification and Error Recovery (R34-T058).

Extends 3.1 Networking key concepts.
Uses the standard ipaddress library to classify local IP addresses against an allowlisted CIDR.
Performs NO active scanning or packet transmission.
Exercises documented invalid/missing-data cases, explains errors, and demonstrates recovery.
"""

from __future__ import annotations

import argparse
import ipaddress
import sys
from typing import Any, Dict, List, Optional, Tuple

DEFAULT_ALLOWLIST_CIDR = "192.0.2.0/24"


def classify_ip(
    ip_str: Optional[str],
    network_cidr: str = DEFAULT_ALLOWLIST_CIDR,
) -> Dict[str, Any]:
    """Classify an IP string against an allowlisted CIDR network range.

    Returns a structured dictionary indicating ALLOW, DENY, or ERROR.
    """
    if ip_str is None or not str(ip_str).strip():
        return {
            "status": "ERROR",
            "ip": ip_str,
            "error_type": "MISSING_DATA",
            "message": "IP address cannot be empty or None",
        }

    raw_ip = str(ip_str).strip()

    try:
        network = ipaddress.ip_network(network_cidr, strict=False)
    except ValueError as e:
        return {
            "status": "ERROR",
            "network": network_cidr,
            "error_type": "INVALID_CIDR",
            "message": f"Malformed network CIDR '{network_cidr}': {e}",
        }

    try:
        addr = ipaddress.ip_address(raw_ip)
    except ValueError as e:
        return {
            "status": "ERROR",
            "ip": raw_ip,
            "error_type": "MALFORMED_IP",
            "message": f"Malformed IP address '{raw_ip}': {e}",
        }

    is_member = addr in network
    return {
        "status": "ALLOW" if is_member else "DENY",
        "ip": str(addr),
        "network": str(network),
        "is_member": is_member,
    }


def process_ip_sequence(
    ip_list: List[Optional[str]],
    network_cidr: str = DEFAULT_ALLOWLIST_CIDR,
) -> List[Dict[str, Any]]:
    """Process a sequence of IPs, demonstrating recovery following errors."""
    return [classify_ip(ip, network_cidr) for ip in ip_list]


def run_demonstration(scenario: str) -> int:
    print(f"Scenario: {scenario}")
    network = DEFAULT_ALLOWLIST_CIDR
    print(f"Allowlisted Network: {network}")

    if scenario == "normal":
        # Sequence exercising member, non-member, invalid error, and recovery on next valid input
        sequence = [
            "192.0.2.1",       # Valid member -> ALLOW
            "198.51.100.1",    # Valid non-member -> DENY
            "999.999.999.999", # Malformed IP -> ERROR (MALFORMED_IP)
            "",                # Missing IP -> ERROR (MISSING_DATA)
            "192.0.2.42",      # Valid member -> ALLOW (demonstrates recovery)
        ]

        results = process_ip_sequence(sequence, network)
        for r in results:
            if r["status"] == "ERROR":
                print(f"[{r['status']}] IP: '{r.get('ip')}' -> {r['error_type']}: {r['message']}")
            else:
                print(f"[{r['status']}] IP: {r['ip']} in {r['network']} -> Member: {r['is_member']}")

        assert results[0]["status"] == "ALLOW"
        assert results[1]["status"] == "DENY"
        assert results[2]["status"] == "ERROR" and results[2]["error_type"] == "MALFORMED_IP"
        assert results[3]["status"] == "ERROR" and results[3]["error_type"] == "MISSING_DATA"
        assert results[4]["status"] == "ALLOW", "Recovery on next valid input failed!"
        print("Graceful recovery demonstrated: Parser handled malformed inputs without state corruption.")
        return 0

    elif scenario == "boundary":
        # Subnet boundaries: Network address (192.0.2.0) and broadcast (192.0.2.255)
        boundaries = ["192.0.2.0", "192.0.2.255", "192.0.3.0"]
        results = process_ip_sequence(boundaries, network)
        for r in results:
            print(f"Boundary [{r['status']}] {r['ip']}: is_member={r['is_member']}")
        assert results[0]["is_member"] is True
        assert results[1]["is_member"] is True
        assert results[2]["is_member"] is False
        return 0

    elif scenario == "failure":
        print("Failure simulation check: Asserting non-member belongs to allowlist...", file=sys.stderr)
        res = classify_ip("198.51.100.1", network)
        try:
            assert res["status"] == "ALLOW", "Expected 198.51.100.1 to be DENIED"
            return 0
        except AssertionError as err:
            print(f"Expected failure caught: {err}", file=sys.stderr)
            return 1

    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Network Range Classification Example")
    parser.add_argument(
        "--scenario",
        choices=["normal", "boundary", "failure"],
        default="normal",
        help="Scenario mode to execute",
    )
    args = parser.parse_args()
    return run_demonstration(args.scenario)


if __name__ == "__main__":
    sys.exit(main())
