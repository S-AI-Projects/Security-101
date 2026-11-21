

# 1. Define client and server capabilities
client_capabilities = {"tools", "resources"}
server_capabilities = {"tools", "prompts"}


# 2. Negotiate common capabilities
def negotiate_capabilities(client, server):
    return client & server


# 3. Dispatch only if the capability was negotiated
def dispatch_request(capability, negotiated, handler):
    if capability not in negotiated:
        raise PermissionError(
            f"Access denied: '{capability}' was not negotiated"
        )

    return handler()


# 4. Local tool handler (simulation)
def tool_handler():
    return "Tool executed successfully!"


# 5. Run the example
if __name__ == "__main__":
    negotiated = negotiate_capabilities(
        client_capabilities,
        server_capabilities
    )

    print("Negotiated capabilities:", sorted(negotiated))

    # Tools are allowed
    result = dispatch_request("tools", negotiated, tool_handler)
    print(result)
    try:
        dispatch_request("resources", negotiated, tool_handler)
    except PermissionError as error:
        print(error)
