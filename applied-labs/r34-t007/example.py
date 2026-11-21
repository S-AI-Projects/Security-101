"""
Cybersecurity Threats Scenario Rubric (Task R34-T007)
Extends 1.2 Common cybersecurity threats with worked input/output rubric checks.
"""
import sys
import json
import argparse

PHYSICAL_SECURITY_KEYWORDS = ["degaussing", "turnstile", "shredder", "guard", "fence", "badge"]

def evaluate_threat_scenario(scenario):
    """
    Evaluates scenario completeness and relevance.
    """
    if not isinstance(scenario, dict):
        return {"status": "FAIL", "message": "Input must be a dictionary object."}

    for req in ["asset", "threat", "control", "residual_risk"]:
        val = scenario.get(req)
        if not val or not str(val).strip():
            return {"status": "FAIL", "missing_field": req, "message": f"Missing required field '{req}'."}

    threat = str(scenario["threat"]).lower()
    control = str(scenario["control"]).lower()

    if any(k in control for k in PHYSICAL_SECURITY_KEYWORDS) and any(k in threat for k in ["phishing", "malware", "ddos", "injection"]):
        return {
            "status": "FLAGGED_FOR_REVIEW",
            "message": "Flagged for review: Physical control does not mitigate network/software threat."
        }

    return {"status": "PASS", "message": "Scenario is complete and internally consistent."}

def get_scenarios():
    return {
        "normal": {
            "asset": "Corporate Employee Laptops",
            "threat": "Spear-phishing attachment executing ransomware payload",
            "control": "Endpoint Detection and Response (EDR) and automated email sandboxing",
            "residual_risk": "Polymorphic payload execution prior to detection signature update"
        },
        "missing_asset": {
            "asset": "",
            "threat": "Credential stuffing attack against corporate portal",
            "control": "Account lockout threshold and mandatory MFA",
            "residual_risk": "MFA prompt fatigue attack"
        },
        "unrelated_control": {
            "asset": "Corporate Mail Server",
            "threat": "Distributed Denial of Service (DDoS) syn-flood",
            "control": "Quarterly hard drive physical degaussing in basement storage",
            "residual_risk": "Improper magnetic degaussing calibration"
        }
    }

def main():
    parser = argparse.ArgumentParser(description="Cybersecurity Threat Scenario Rubric")
    parser.add_argument("--scenario", choices=["normal", "missing_asset", "unrelated_control", "all"], default="all")
    args = parser.parse_args()

    scenarios = get_scenarios()
    if args.scenario == "all":
        results = {name: evaluate_threat_scenario(sc) for name, sc in scenarios.items()}
        print(json.dumps(results, indent=2))
    else:
        print(json.dumps(evaluate_threat_scenario(scenarios[args.scenario]), indent=2))

if __name__ == "__main__":
    main()
