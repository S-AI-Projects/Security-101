import os, sys, argparse
current_dir = os.path.dirname(os.path.abspath(__file__))
repo_root = os.path.dirname(os.path.dirname(current_dir))
sys.path.insert(0, os.path.join(repo_root, "applied-labs", "r34-t003"))

from example import dispatch_tool, reference_calculator

def run_checks(deliberate_wrong=False):
    # Check 1: add(2,3) -> 5
    r1 = dispatch_tool({"tool": "add", "a": 2, "b": 3})
    if deliberate_wrong:
        assert r1["result"] == 999, "DELIBERATE WRONG RESULT: forced assertion failure"
    else:
        assert r1["result"] == 5, f"Expected 5, got {r1.get('result')}"
    
    # Check 2: multiply(2,3) -> 6
    r2 = dispatch_tool({"tool": "multiply", "a": 2, "b": 3})
    assert r2["result"] == 6, f"Expected 6, got {r2.get('result')}"
    
    # Check 3: unknown tool structured error
    r3 = dispatch_tool({"tool": "unknown", "a": 2, "b": 3})
    assert r3["status"] == "error" and r3["error_type"] == "UNKNOWN_TOOL"
    
    # Check 4: string arg structured error
    r4 = dispatch_tool({"tool": "add", "a": "text", "b": 3})
    assert r4["status"] == "error" and r4["error_type"] == "INVALID_ARGUMENT"
    
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
