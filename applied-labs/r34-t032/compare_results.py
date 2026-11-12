
from example import negotiate_capabilities, invoke_capability


# Same fixture as example.py
client = {"tools", "resources"}
server = {"tools", "prompts"}

negotiated = negotiate_capabilities(client, server)


# Independent expected results
expected_results = {
    "negotiated": {"tools"},
    "tools": "DISPATCHED: tools",
    "resources": "REJECTED",
    "prompts": "REJECTED",
    "unknown": "REJECTED"
}


def dispatch(capability):
    return f"DISPATCHED: {capability}"


actual_results = {
    "negotiated": negotiated,
    "tools": invoke_capability("tools", negotiated, dispatch),
    "resources": invoke_capability("resources", negotiated, dispatch),
    "prompts": invoke_capability("prompts", negotiated, dispatch),
    "unknown": invoke_capability("unknown", negotiated, dispatch)
}


all_passed = True

for case, expected in expected_results.items():
    actual = actual_results[case]

    print(f"\nCase: {case}")
    print("Expected:", expected)
    print("Actual:  ", actual)

    if actual != expected:
        print("RESULT: FAIL")
        all_passed = False
    else:
        print("RESULT: PASS")


if not all_passed:
    raise SystemExit("Comparison failed!")

print("\nAll expected results match.")

