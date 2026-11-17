"""Zero Trust Capability Negotiation and Feature Gating (R34-T052).

Extends 3.2 Networking zero trust architecture.
Demonstrates Zero Trust capability negotiation by intersecting client and server
advertised capabilities, rejecting any invocation outside the negotiated set before dispatch.
"""

from __future__ import annotations

import argparse
import sys
from typing import Any, Dict, Optional, Set, Tuple


class CapabilityNotNegotiatedError(Exception):
    """Raised when an unnegotiated capability is invoked."""
    pass


def negotiate_capabilities(client_caps: Set[str], server_caps: Set[str]) -> Set[str]:
    """Negotiate capabilities by taking the strict intersection of client and server sets."""
    return set(client_caps) & set(server_caps)


def dispatch_capability(
    negotiated: Set[str],
    capability: str,
    payload: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Dispatch a capability call only if it exists within the negotiated set.

    Rejects unnegotiated capabilities prior to executing any handler.
    """
    if capability not in negotiated:
        raise CapabilityNotNegotiatedError(
            f"Capability '{capability}' was not negotiated. Negotiated capabilities: {sorted(list(negotiated))}"
        )

    # Simulated local handlers
    handlers = {
        "tools": lambda p: {"status": "SUCCESS", "capability": "tools", "data": "tool_catalog_v1"},
        "resources": lambda p: {"status": "SUCCESS", "capability": "resources", "data": "resource_index_v1"},
        "prompts": lambda p: {"status": "SUCCESS", "capability": "prompts", "data": "prompt_templates_v1"},
    }

    handler = handlers.get(capability, lambda p: {"status": "SUCCESS", "capability": capability, "data": "generic_ack"})
    return handler(payload or {})


def safe_dispatch(
    negotiated: Set[str],
    capability: str,
    payload: Optional[Dict[str, Any]] = None,
) -> Tuple[str, Dict[str, Any]]:
    """Safely attempts dispatch, capturing rejection as structured status."""
    try:
        result = dispatch_capability(negotiated, capability, payload)
        return "SUCCESS", result
    except CapabilityNotNegotiatedError as e:
        return "REJECTED", {"error": str(e), "capability": capability}


def run_demonstration(scenario: str) -> int:
    print(f"Scenario: {scenario}")
    if scenario == "normal":
        client_caps = {"tools", "resources"}
        server_caps = {"tools", "prompts"}
        negotiated = negotiate_capabilities(client_caps, server_caps)
        print(f"Client caps: {sorted(list(client_caps))}")
        print(f"Server caps: {sorted(list(server_caps))}")
        print(f"Negotiated caps (intersection): {sorted(list(negotiated))}")

        # 1. Dispatching negotiated 'tools'
        status_tools, res_tools = safe_dispatch(negotiated, "tools")
        print(f"Dispatch 'tools': [{status_tools}] -> {res_tools}")

        # 2. Dispatching unnegotiated 'resources'
        status_res, res_res = safe_dispatch(negotiated, "resources")
        print(f"Dispatch 'resources': [{status_res}] -> {res_res}")

        assert status_tools == "SUCCESS"
        assert status_res == "REJECTED"
        return 0

    elif scenario == "boundary":
        # Boundary case: Disjoint capability sets yield empty negotiation set
        client_caps = {"resources"}
        server_caps = {"prompts"}
        negotiated = negotiate_capabilities(client_caps, server_caps)
        print(f"Client caps: {sorted(list(client_caps))}")
        print(f"Server caps: {sorted(list(server_caps))}")
        print(f"Negotiated caps (empty boundary): {sorted(list(negotiated))}")

        status, res = safe_dispatch(negotiated, "resources")
        print(f"Dispatch 'resources' on empty negotiation: [{status}] -> {res}")
        assert len(negotiated) == 0
        assert status == "REJECTED"
        return 0

    elif scenario == "failure":
        # Failure case: Unhandled unnegotiated dispatch raises error and exits 1
        client_caps = {"tools"}
        server_caps = {"tools"}
        negotiated = negotiate_capabilities(client_caps, server_caps)
        print("Executing unnegotiated dispatch expecting failure exit...", file=sys.stderr)
        try:
            dispatch_capability(negotiated, "resources")
            return 0
        except CapabilityNotNegotiatedError as err:
            print(f"Expected failure caught: {err}", file=sys.stderr)
            return 1

    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Zero Trust Capability Negotiation Example")
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
