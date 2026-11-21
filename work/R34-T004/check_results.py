import os, sys, argparse
current_dir = os.path.dirname(os.path.abspath(__file__))
repo_root = os.path.dirname(os.path.dirname(current_dir))
sys.path.insert(0, os.path.join(repo_root, "applied-labs", "r34-t004"))

from example import negotiate_capabilities, invoke_capability

def run_checks(deliberate_wrong=False):
    client_caps = {"tools", "resources"}
    server_caps = {"tools", "prompts"}
    negotiated, trace = negotiate_capabilities(client_caps, server_caps)
    
    # Check 1: Negotiation result
    assert negotiated == {"tools"}, f"Expected {{'tools'}}, got {negotiated}"
    
    # Check 2: Calling unnegotiated resources rejected
    res_resources = invoke_capability(negotiated, "resources")
    if deliberate_wrong:
        assert res_resources["status"] == "DISPATCHED", "DELIBERATE WRONG RESULT: forced assertion failure"
    else:
        assert res_resources["status"] == "REJECTED", f"Expected REJECTED, got {res_resources['status']}"
        assert not res_resources["dispatched"], "Unnegotiated capability was incorrectly dispatched"
    
    # Check 3: Calling negotiated tools passes
    res_tools = invoke_capability(negotiated, "tools")
    assert res_tools["status"] == "DISPATCHED" and res_tools["dispatched"]
    print("All assertion checks passed successfully.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--deliberate-wrong-result", action="store_true", help="Force failure")
    args = parser.parse_args()
    try:
        run_checks(deliberate_wrong=args.deliberate_wrong_result)
        sys.exit(0)
    except AssertionError as e:
        print(f"Assertion Error: {e}", file=sys.stderr)
        sys.exit(1)
