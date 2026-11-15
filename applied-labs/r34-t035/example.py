import json
from pathlib import Path
def baseline_negotiate(client, server):
    """Original implementation: find shared capabilities."""
    return {
        capability
        for capability in client
        if capability in server
    }


def extract_shared_capabilities(client, server):
    """Extract the shared-capability calculation into one responsibility."""
    return set(client.keys()) & set(server.keys())


def negotiate(client, server):
    """Refactored implementation."""
    return extract_shared_capabilities(client, server)


def dispatch(capability, negotiated, dispatch_log):
    """Reject a capability before dispatch if it was not negotiated."""
    if capability not in negotiated:
        raise PermissionError(
            f"Capability '{capability}' was not negotiated"
        )

    dispatch_log.append(capability)
    return f"{capability} dispatched"


def main():
    client = {
        "tools": True,
        "resources": True,
    }

    server = {
        "tools": True,
        "prompts": True,
    }

    baseline = baseline_negotiate(client, server)
    actual = negotiate(client, server)

    print("Baseline:", sorted(baseline))
    print("Refactored:", sorted(actual))
    print("Equivalent:", baseline == actual)

    dispatch_log = []

    print("Tools:", dispatch("tools", actual, dispatch_log))

    try:
        dispatch("resources", actual, dispatch_log)
    except PermissionError as error:
        print("Resources rejected:", error)
    actual_results = {
        "negotiated": sorted(actual),
        "baseline_equivalent": baseline == actual,
        "tools_dispatched": "tools" in dispatch_log,
        "resources_rejected": "resources" not in dispatch_log,
        "dispatch_log": dispatch_log,
    }

    Path("work/R34-T035/actual.json").write_text(
        json.dumps(actual_results, indent=2) + "\n"
    )
    print("Dispatch log:", dispatch_log)


if __name__ == "__main__":
    main()
