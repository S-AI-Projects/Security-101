
def negotiate_capabilities(client, server):
    """Find capabilities supported by both client and server."""
    return client & server



def invoke_capability(capability, negotiated, dispatch):
    """Reject capabilities that were not negotiated."""
    if capability not in negotiated:
        return "REJECTED"

    return dispatch(capability)



# Small local fixture for the assignment
client_capabilities = {"tools", "resources"}
server_capabilities = {"tools", "prompts"}

# Only common capabilities are negotiated
negotiated_capabilities = negotiate_capabilities(
    client_capabilities,
    server_capabilities
)


def dispatch(capability):
    """Simulate executing an allowed capability."""
    return f"DISPATCHED: {capability}"


if __name__ == "__main__":
    print("Negotiated capabilities:", negotiated_capabilities)

    print(
        "Tools request:",
        invoke_capability("tools", negotiated_capabilities, dispatch)
    )

    print(
        "Resources request:",
        invoke_capability("resources", negotiated_capabilities, dispatch)
    )

    print(
        "Prompts request:",
        invoke_capability("prompts", negotiated_capabilities, dispatch)
    )

    print(
        "Unknown request:",
        invoke_capability("unknown", negotiated_capabilities, dispatch)
    )
