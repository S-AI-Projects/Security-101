"""Deterministic capability-negotiation mock for R34-T024.

The example illustrates capability discovery and least-privilege feature gating.
It is local and performs no network or real service calls.
"""

from __future__ import annotations

import argparse
import sys
from typing import Protocol


LESSON_CITATION = "3.2 Networking zero trust architecture.md"
CLIENT_CAPABILITIES = frozenset({"tools", "resources"})
SERVER_CAPABILITIES = frozenset({"tools", "prompts"})


class CapabilityService(Protocol):
    """Callable interface for the external capability dependency."""

    def negotiate(self, client: frozenset[str]) -> frozenset[str]:
        ...

    def dispatch(self, capability: str) -> str:
        ...


class LocalCapabilityAdapter:
    """Deterministic local adapter with no network or external service."""

    def __init__(self, server_capabilities: frozenset[str]) -> None:
        self.server_capabilities = server_capabilities
        self.dispatch_count = 0

    def negotiate(self, client: frozenset[str]) -> frozenset[str]:
        return client.intersection(self.server_capabilities)

    def dispatch(self, capability: str) -> str:
        self.dispatch_count += 1
        return f"dispatched:{capability}"


class CapabilityGate:
    """Reject non-negotiated capabilities before dispatch."""

    def __init__(self, service: CapabilityService) -> None:
        self.service = service

    def negotiate_and_call(self, client: frozenset[str], capability: str) -> str:
        negotiated = self.service.negotiate(client)
        if capability not in negotiated:
            raise PermissionError(
                f"Capability {capability!r} was not negotiated; allowed={sorted(negotiated)}"
            )
        return self.service.dispatch(capability)


def negotiate(client: frozenset[str], server: frozenset[str]) -> frozenset[str]:
    """Return the set intersection, preserving one named responsibility."""
    return client.intersection(server)


def run_scenario(scenario: str) -> tuple[int, str]:
    adapter = LocalCapabilityAdapter(SERVER_CAPABILITIES)
    gate = CapabilityGate(adapter)

    if scenario == "normal":
        negotiated = gate.service.negotiate(CLIENT_CAPABILITIES)
        if negotiated != frozenset({"tools"}):
            return 1, "Unexpected negotiated capabilities"
        dispatched = gate.negotiate_and_call(CLIENT_CAPABILITIES, "tools")
        output = (
            f'Scenario: capability intersection based on "{LESSON_CITATION}".\n'
            f"client={sorted(CLIENT_CAPABILITIES)}\n"
            f"server={sorted(SERVER_CAPABILITIES)}\n"
            f"negotiated={sorted(negotiated)}\n"
            f"tools result={dispatched}"
        )
        return 0, output

    if scenario == "boundary":
        negotiated = negotiate(CLIENT_CAPABILITIES, SERVER_CAPABILITIES)
        empty_overlap = negotiate(frozenset({"resources"}), frozenset({"prompts"}))
        output = (
            f'Scenario: boundary intersection based on "{LESSON_CITATION}".\n'
            f"fixture_overlap={sorted(negotiated)}\n"
            f"empty_overlap={sorted(empty_overlap)}"
        )
        expected = negotiated == frozenset({"tools"}) and empty_overlap == frozenset()
        return (0, output) if expected else (1, "Unexpected boundary result")

    if scenario == "failure":
        before = adapter.dispatch_count
        try:
            gate.negotiate_and_call(CLIENT_CAPABILITIES, "resources")
            return 1, "Unexpected success for resources"
        except PermissionError as exc:
            if adapter.dispatch_count != before:
                return 1, "Rejected capability was dispatched"
            return 1, f'Scenario: pre-dispatch rejection based on "{LESSON_CITATION}".\nError: {exc}'

    if scenario == "explain":
        negotiated = negotiate(CLIENT_CAPABILITIES, SERVER_CAPABILITIES)
        before = adapter.dispatch_count
        try:
            gate.negotiate_and_call(CLIENT_CAPABILITIES, "resources")
        except PermissionError:
            pass
        output = (
            f"Worked fixture for {LESSON_CITATION}\n"
            f"client={sorted(CLIENT_CAPABILITIES)}\n"
            f"server={sorted(SERVER_CAPABILITIES)}\n"
            f"negotiated={sorted(negotiated)}\n"
            "resources result=rejected_before_dispatch\n"
            f"dispatch_count={adapter.dispatch_count - before}"
        )
        return 0, output

    return 1, f"Unknown scenario: {scenario}"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Local capability-negotiation and feature-gating simulation."
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
