import os, sys, argparse
current_dir = os.path.dirname(os.path.abspath(__file__))
repo_root = os.path.dirname(os.path.dirname(current_dir))
sys.path.insert(0, os.path.join(repo_root, "applied-labs", "r34-t005"))

from example import LocalOfflineSecurityAdapter, get_fictional_scenarios

def run_checks(deliberate_wrong=False):
    adapter = LocalOfflineSecurityAdapter()
    scenarios = get_fictional_scenarios()
    
    r1 = adapter.evaluate(scenarios["normal"])
    if deliberate_wrong:
        assert r1["status"] == "FAIL", "DELIBERATE WRONG RESULT: forced assertion failure"
    else:
        assert r1["status"] == "PASS", f"Expected PASS, got {r1['status']}"
        
    r2 = adapter.evaluate(scenarios["missing_asset"])
    assert r2["status"] == "FAIL" and r2.get("missing_field") == "asset"
    
    r3 = adapter.evaluate(scenarios["unrelated_control"])
    assert r3["status"] == "FLAGGED_FOR_REVIEW"
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
