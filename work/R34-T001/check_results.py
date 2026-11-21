import os, sys, argparse

current_dir = os.path.dirname(os.path.abspath(__file__))
repo_root = os.path.dirname(os.path.dirname(current_dir))
sys.path.insert(0, os.path.join(repo_root, "applied-labs", "r34-t001"))

from example import check_scenario, get_fictional_scenarios

def run_checks(deliberate_wrong=False):
    scenarios = get_fictional_scenarios()
    res_normal = check_scenario(scenarios['normal'])
    if deliberate_wrong:
        assert res_normal['status'] == 'FAIL', 'DELIBERATE WRONG RESULT: forced assertion failure'
    else:
        assert res_normal['status'] == 'PASS', f"Expected PASS, got {res_normal['status']}"
    
    res_missing = check_scenario(scenarios['missing_asset'])
    assert res_missing['status'] == 'FAIL', f"Expected FAIL, got {res_missing['status']}"
    
    res_unrelated = check_scenario(scenarios['unrelated_control'])
    assert res_unrelated['status'] == 'FLAGGED_FOR_REVIEW', f"Expected FLAGGED_FOR_REVIEW, got {res_unrelated['status']}"
    print('All assertion checks passed successfully.')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--deliberate-wrong-result', action='store_true', help='Force failure')
    args = parser.parse_args()
    try:
        run_checks(deliberate_wrong=args.deliberate_wrong_result)
        sys.exit(0)
    except AssertionError as e:
        print(f'Assertion Error: {e}', file=sys.stderr)
        sys.exit(1)
