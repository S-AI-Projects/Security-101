import os, sys, argparse
current_dir = os.path.dirname(os.path.abspath(__file__))
repo_root = os.path.dirname(os.path.dirname(current_dir))
sys.path.insert(0, os.path.join(repo_root, "applied-labs", "r34-t006"))

from example import ActionExecutorStub, refactored_execute

def run_checks(deliberate_wrong=False):
    ex = ActionExecutorStub()
    
    # Check 1: Allowed read passes
    r1 = refactored_execute({"tool": "read_document", "args": {"path": "/docs/test.txt"}}, ex)
    if deliberate_wrong:
        assert r1["status"] == "REJECTED", "DELIBERATE WRONG RESULT: forced assertion failure"
    else:
        assert r1["status"] == "EXECUTED", f"Expected EXECUTED, got {r1['status']}"
        assert len(ex.executed_actions) == 1
        
    # Check 2: Unknown delete tool rejected
    r2 = refactored_execute({"tool": "delete_document", "args": {"path": "/docs/test.txt"}}, ex)
    assert r2["status"] == "REJECTED"
    assert len(ex.executed_actions) == 1  # Did not reach executor
    
    # Check 3: Missing path rejected
    r3 = refactored_execute({"tool": "read_document", "args": {}}, ex)
    assert r3["status"] == "REJECTED"
    assert len(ex.executed_actions) == 1
    
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
