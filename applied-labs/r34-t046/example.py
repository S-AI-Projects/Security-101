"""Gate mock identity service requests on negotiated capabilities."""

from collections.abc import Callable

CLIENT = frozenset({"tools", "resources"})
SERVER = frozenset({"tools", "prompts"})


def negotiate(client: frozenset[str], server: frozenset[str]) -> frozenset[str]:
    """Return the capabilities both peers advertise."""
    return client & server


def dispatch(
    client: frozenset[str],
    server: frozenset[str],
    capability: str,
    handle: Callable[[str], str],
) -> str:
    if capability not in negotiate(client, server):
        return "REJECTED (unnegotiated capability)"
    return handle(capability)


def mock_handler(capability: str) -> str:
    return f"ACCEPTED (mock {capability} handler)"


if __name__ == "__main__":
    print(f"Negotiated: {sorted(negotiate(CLIENT, SERVER))}")
    for capability in ("tools", "resources"):
        print(f"{capability}: {dispatch(CLIENT, SERVER, capability, mock_handler)}")
