import os, sys, argparse
current_dir = os.path.dirname(os.path.abspath(__file__))
repo_root = os.path.dirname(os.path.dirname(current_dir))
sys.path.insert(0, os.path.join(repo_root, "applied-labs", "r34-t010"))

from example import evaluate_ai_action, StubActionExecutor

def run_checks(deliberate_wrong=False):
    ex = StubActionExecutor()
    
    # Check 1: Allowed read passes
    r1 = evaluate_ai_action({"tool": "read", "args": {"path": "file.txt"}}, ex)
    if deliberate_wrong:
        assert r1["status"] == "REJECTED", "DELIBERATE WRONG RESULT: forced assertion failure"
    else:
        assert r1["status"] == "ALLOWED", f"Expected ALLOWED, got {r1['status']}"
        assert ex.call_count == 1
        
    # Check 2: Unknown delete tool rejected
    r2 = evaluate_ai_action({"tool": "delete", "args": {"path": "file.txt"}}, ex)
    assert r2["status"] == "REJECTED"
    assert ex.call_count == 1
    
    # Check 3: Missing arg rejected
    r3 = evaluate_ai_action({"tool": "read", "args": {}}, ex)
    assert r3["status"] == "REJECTED"
    assert ex.call_count == 1
    
    print("All assertion checks passed successfully.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--deliberate-wrong-result", action="store_true")
    args = parser.parse_args()
    try:
        run_checks(deliberate_wrong=args.deliberate_wrong_result)
        sys.exit(0)
    except AssertionError as e:
        print(f"Assertion Error: {e}", file=sys.stderr)
        sys.exit(1)
