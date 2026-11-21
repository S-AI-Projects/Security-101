"""
SecOps Quiz Scenario Evaluator with Recovery (Task R34-T008)
Evaluates SecOps scenarios, exercising failure on invalid data and clean recovery on subsequent valid inputs.
"""
import sys
import json
import argparse

PHYSICAL_SECURITY_KEYWORDS = ["patrol", "gate", "badge", "turnstile", "fence"]

def evaluate_scenario(scenario):
    if not isinstance(scenario, dict):
        return {"status": "FAIL", "error": "Invalid format: Scenario must be a dictionary."}

    for req in ["asset", "threat", "control", "residual_risk"]:
        val = scenario.get(req)
        if not val or not str(val).strip():
            return {"status": "FAIL", "missing_field": req, "error": f"Validation error: Missing required field '{req}'."}

    threat = str(scenario["threat"]).lower()
    control = str(scenario["control"]).lower()

    if any(k in control for k in PHYSICAL_SECURITY_KEYWORDS) and any(k in threat for k in ["siem", "soc", "malware", "alert", "incident", "phishing", "exfiltration"]):
        return {
            "status": "FLAGGED_FOR_REVIEW",
            "error": "Flagged for review: Physical control does not mitigate digital SecOps threat."
        }

    return {"status": "PASS", "message": "SecOps scenario validated successfully."}

def process_scenario_stream(scenario_list):
    """
    Demonstrates clean error handling: processing an invalid scenario reports failure,
    and processing the next valid scenario recovers and succeeds without crashing.
    """
    results = []
    for item in scenario_list:
        res = evaluate_scenario(item)
        results.append(res)
    return results

def get_scenarios():
    return {
        "normal": {
            "asset": "Centralized SIEM Log Aggregator",
            "threat": "Log injection attack attempting to forge audit trails",
            "control": "Cryptographic log signing and immutable WORM storage",
            "residual_risk": "Compromised log ingestion certificate"
        },
        "missing_asset": {
            "asset": "",
            "threat": "Alert fatigue blinding analysts to active malware",
            "control": "SOAR automated triage and deduplication playbooks",
            "residual_risk": "Over-filtering of novel attack patterns"
        },
        "unrelated_control": {
            "asset": "Security Operations Center (SOC) Workstation",
            "threat": "Phishing-based credential exfiltration of analyst session",
            "control": "Security turnstiles at facility entrance",
            "residual_risk": "Physical badge cloning"
        }
    }

def main():
    parser = argparse.ArgumentParser(description="SecOps Scenario Evaluator with Recovery")
    parser.add_argument("--scenario", choices=["normal", "missing_asset", "unrelated_control", "stream"], default="stream")
    args = parser.parse_args()

    scenarios = get_scenarios()
    if args.scenario == "stream":
        stream = [scenarios["missing_asset"], scenarios["normal"]]
        print(json.dumps(process_scenario_stream(stream), indent=2))
    else:
        print(json.dumps(evaluate_scenario(scenarios[args.scenario]), indent=2))

if __name__ == "__main__":
    main()
