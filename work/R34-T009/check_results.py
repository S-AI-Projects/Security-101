import os, sys, argparse
current_dir = os.path.dirname(os.path.abspath(__file__))
repo_root = os.path.dirname(os.path.dirname(current_dir))
sys.path.insert(0, os.path.join(repo_root, "applied-labs", "r34-t009"))

from example import validate_and_redact_config

def run_checks(deliberate_wrong=False):
    # Check 1: Valid config
    valid_cfg = {"command": "python3", "args": ["-v"], "env": {"TOKEN": "secret"}}
    r1 = validate_and_redact_config(valid_cfg)
    if deliberate_wrong:
        assert r1["status"] == "FAIL", "DELIBERATE WRONG RESULT: forced assertion failure"
    else:
        assert r1["status"] == "PASS"
        assert r1["validated_configuration"]["redacted_env"]["TOKEN"] == "[REDACTED]"
        assert not r1["process_launched"]
        
    # Check 2: Missing command fails
    r2 = validate_and_redact_config({"command": "", "args": []})
    assert r2["status"] == "FAIL"
    
    # Check 3: Single string args fails
    r3 = validate_and_redact_config({"command": "node", "args": "index.js"})
    assert r3["status"] == "FAIL"
    
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
