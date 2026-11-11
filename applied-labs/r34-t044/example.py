"""Capability negotiation and zero trust dispatch gate."""

from typing import Any

# Example capability handlers
def handle_tools(payload: dict[str, Any]) -> dict[str, Any]:
    """Execute tools capability handler."""
    action = payload.get("action", "inspect")
    return {"status": "SUCCESS", "capability": "tools", "output": f"Executed tool action: {action}"}


def handle_resources(payload: dict[str, Any]) -> dict[str, Any]:
    """Resource handler (should be gated if not negotiated)."""
    uri = payload.get("uri", "internal://logs")
    return {"status": "SUCCESS", "capability": "resources", "output": f"Accessed resource: {uri}"}


def handle_prompts(payload: dict[str, Any]) -> dict[str, Any]:
    """Prompt handler (should be gated if not negotiated)."""
    name = payload.get("name", "audit")
    return {"status": "SUCCESS", "capability": "prompts", "output": f"Loaded prompt: {name}"}


CAPABILITY_HANDLERS = {
    "tools": handle_tools,
    "resources": handle_resources,
    "prompts": handle_prompts,
}


class ZeroTrustSession:
    """Session managing negotiated capabilities and enforcement gating."""

    def __init__(self, client_caps: set[str], server_caps: set[str]) -> None:
        self.client_caps = set(client_caps)
        self.server_caps = set(server_caps)
        # Negotiate intersection
        self.negotiated = self.client_caps.intersection(self.server_caps)

    def dispatch(self, capability: str, payload: dict[str, Any]) -> dict[str, Any]:
        """Dispatch invocation to handler only if capability is negotiated."""
        if capability not in self.negotiated:
            return {
                "status": "REJECTED",
                "capability": capability,
                "error": {
                    "code": "UNNEGOTIATED_CAPABILITY",
                    "message": f"Capability '{capability}' was not negotiated for this session",
                },
            }

        handler = CAPABILITY_HANDLERS.get(capability)
        if handler is None:
            return {
                "status": "ERROR",
                "capability": capability,
                "error": {
                    "code": "HANDLER_NOT_FOUND",
                    "message": f"No handler registered for '{capability}'",
                },
            }

        return handler(payload)


# Standard scenario fixtures
FIXTURES = {
    "standard-negotiation": {
        "client_caps": {"tools", "resources"},
        "server_caps": {"tools", "prompts"},
        "calls": [
            ("tools", {"action": "query_siem"}),
            ("resources", {"uri": "file:///var/log/audit.log"}),
        ],
    },
    "all-rejected": {
        "client_caps": {"resources"},
        "server_caps": {"tools", "prompts"},
        "calls": [
            ("resources", {"uri": "file:///etc/hosts"}),
        ],
    },
    "full-intersection": {
        "client_caps": {"tools", "prompts", "resources"},
        "server_caps": {"tools", "prompts", "resources"},
        "calls": [
            ("tools", {"action": "run_scan"}),
            ("prompts", {"name": "summarize_incident"}),
            ("resources", {"uri": "s3://backups"}),
        ],
    },
}


def run_session_fixture(fixture: dict[str, Any]) -> dict[str, Any]:
    """Execute session negotiation and dispatch calls for a fixture."""
    session = ZeroTrustSession(fixture["client_caps"], fixture["server_caps"])
    results = []
    for cap, payload in fixture["calls"]:
        res = session.dispatch(cap, payload)
        results.append(res)
    return {
        "negotiated": sorted(session.negotiated),
        "results": results,
    }


if __name__ == "__main__":
    report = run_session_fixture(FIXTURES["standard-negotiation"])
    print(f"Negotiated capabilities: {report['negotiated']}")
    for res in report["results"]:
        status = res["status"]
        cap = res["capability"]
        if status == "SUCCESS":
            print(f"Call to '{cap}': status={status}, output={res['output']}")
        else:
            err = res["error"]["code"]
            print(f"Call to '{cap}': status={status}, error={err}")
