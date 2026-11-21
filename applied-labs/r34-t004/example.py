"""
Zero Trust Capability Negotiation (Task R34-T004)
Negotiates mutual capabilities between client and server via set intersection.
Rejects unnegotiated capability invocation before dispatch.
"""
import sys
import json
import argparse

def negotiate_capabilities(client_caps, server_caps):
    """
    Intersects client and server capability sets.
    Records intermediate trace steps.
    """
    client_set = set(client_caps)
    server_set = set(server_caps)
    negotiated = client_set.intersection(server_set)
    
    trace = {
        "step_1_client_offered": sorted(list(client_set)),
        "step_2_server_supported": sorted(list(server_set)),
        "step_3_negotiated": sorted(list(negotiated))
    }
    return negotiated, trace

def invoke_capability(negotiated_caps, requested_cap, payload=None):
    """
    Dispatches request only if requested_cap is in negotiated_caps.
    Rejects prior to execution if capability was not negotiated.
    """
    if requested_cap not in negotiated_caps:
        return {
            "status": "REJECTED",
            "dispatched": False,
            "capability": requested_cap,
            "reason": f"Capability '{requested_cap}' was not negotiated."
        }

    # Deterministic local dispatch
    return {
        "status": "DISPATCHED",
        "dispatched": True,
        "capability": requested_cap,
        "payload": payload or {}
    }

def main():
    parser = argparse.ArgumentParser(description="Zero Trust Capability Negotiation")
    parser.add_argument("--request", choices=["tools", "resources", "prompts"], default="tools")
    args = parser.parse_args()

    client_caps = ["tools", "resources"]
    server_caps = ["tools", "prompts"]

    negotiated, trace = negotiate_capabilities(client_caps, server_caps)
    result = invoke_capability(negotiated, args.request, {"action": "query"})
    
    output = {
        "negotiation_trace": trace,
        "invocation_result": result
    }
    print(json.dumps(output, indent=2))

if __name__ == "__main__":
    main()
