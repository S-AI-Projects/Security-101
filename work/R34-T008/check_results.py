import os, sys, argparse
current_dir = os.path.dirname(os.path.abspath(__file__))
repo_root = os.path.dirname(os.path.dirname(current_dir))
sys.path.insert(0, os.path.join(repo_root, "applied-labs", "r34-t008"))

from example import evaluate_scenario, process_scenario_stream, get_scenarios

def run_checks(deliberate_wrong=False):
    sc = get_scenarios()
    r1 = evaluate_scenario(sc["normal"])
    if deliberate_wrong:
        assert r1["status"] == "FAIL", "DELIBERATE WRONG RESULT: forced assertion failure"
    else:
        assert r1["status"] == "PASS", f"Expected PASS, got {r1['status']}"
        
    r2 = evaluate_scenario(sc["missing_asset"])
    assert r2["status"] == "FAIL" and r2["missing_field"] == "asset"
    
    # Recovery check
    stream_res = process_scenario_stream([sc["missing_asset"], sc["normal"]])
    assert stream_res[0]["status"] == "FAIL"
    assert stream_res[1]["status"] == "PASS"
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
