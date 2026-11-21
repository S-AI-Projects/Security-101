import os, sys, argparse
current_dir = os.path.dirname(os.path.abspath(__file__))
repo_root = os.path.dirname(os.path.dirname(current_dir))
sys.path.insert(0, os.path.join(repo_root, "applied-labs", "r34-t002"))

from example import evaluate_access

def run_checks(deliberate_wrong=False):
    r1 = evaluate_access("reader", "read", "public")
    if deliberate_wrong:
        assert r1["decision"] == "DENY", "DELIBERATE WRONG RESULT: forced assertion failure"
    else:
        assert r1["decision"] == "ALLOW", f"Expected ALLOW, got {r1['decision']}"
    
    r2 = evaluate_access("reader", "write", "public")
    assert r2["decision"] == "DENY", f"Expected DENY, got {r2['decision']}"
    
    r3 = evaluate_access("auditor", "audit", "logs")
    assert r3["decision"] == "DENY", f"Expected DENY, got {r3['decision']}"
    
    r4 = evaluate_access("unknown_role", "read", "public")
    assert r4["decision"] == "DENY", f"Expected DENY, got {r4['decision']}"
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
