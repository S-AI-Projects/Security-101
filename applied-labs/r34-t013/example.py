"""A local mock of capability negotiation and pre-dispatch gating."""

import argparse
from collections.abc import Callable, Sequence
from typing import AbstractSet


CLIENT_CAPABILITIES = frozenset({"tools", "resources"})
SERVER_CAPABILITIES = frozenset({"tools", "prompts"})


def negotiate_capabilities(
    client_capabilities: AbstractSet[str],
    server_capabilities: AbstractSet[str],
) -> frozenset[str]:
    """Return only capabilities offered by both sides."""
    return frozenset(client_capabilities & server_capabilities)


def dispatch_request(
    capability: str,
    negotiated_capabilities: AbstractSet[str],
    handler: Callable[[], str],
) -> str:
    """Reject unnegotiated capabilities before calling their handler."""
    if capability not in negotiated_capabilities:
        raise PermissionError(f"capability {capability!r} was not negotiated")
    return handler()


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--scenario",
        choices=("normal", "boundary", "failure"),
        default="normal",
        help="run the shared-capability, empty-intersection, or rejected-request case",
    )
    arguments = parser.parse_args(argv)

    client_capabilities = CLIENT_CAPABILITIES
    server_capabilities = SERVER_CAPABILITIES
    requested_capability = "tools"
    if arguments.scenario == "boundary":
        client_capabilities = frozenset({"resources"})
    elif arguments.scenario == "failure":
        requested_capability = "resources"

    negotiated = negotiate_capabilities(
        client_capabilities,
        server_capabilities,
    )

    print(f"Scenario: {arguments.scenario} (local mock)")
    print(f"Client capabilities: {sorted(client_capabilities)}")
    print(f"Server capabilities: {sorted(server_capabilities)}")
    print(f"Negotiated capabilities: {sorted(negotiated)}")

    handler_called = False

    def handler() -> str:
        nonlocal handler_called
        handler_called = True
        return f"{requested_capability} dispatched"

    try:
        result = dispatch_request(requested_capability, negotiated, handler)
    except PermissionError as error:
        print(f"Rejected: {error}")
        print(f"Handler invoked: {handler_called}")
        return 1

    print(f"Result: {result}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
