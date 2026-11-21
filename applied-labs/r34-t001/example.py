"""
Infrastructure Security Scenario Rubric Checker (Task R34-T001)
Beginner-friendly rubric checker for Module 6: Infrastructure Security.
"""
import sys
import json
import argparse

# Keywords commonly related to infrastructure threats vs controls
THREAT_CONTROL_KEYWORDS = {
    "patch": ["patch", "update", "vulnerability", "scanner", "upgrade"],
    "container": ["container", "image", "isolation", "runtime", "cgroup", "namespace"],
    "network": ["firewall", "segmentation", "bastion", "vpn", "ssh", "tls"],
    "access": ["mfa", "rbac", "least privilege", "credentials", "identity"]
}

PHYSICAL_SECURITY_KEYWORDS = ["turnstile", "badge", "guard", "fence", "door", "gate"]

def check_scenario(scenario):
    """
    Validates an infrastructure security scenario against structural and relevance rubrics.
    
    A scenario must have:
      - asset: non-empty string
      - threat: non-empty string
      - control: non-empty string
      - residual_risk: non-empty string
    
    Returns a dict with 'status' (PASS, FAIL, FLAGGED_FOR_REVIEW) and 'message'.
    """
    if not isinstance(scenario, dict):
        return {"status": "FAIL", "message": "Scenario must be a dictionary object."}

    # 1. Structural check: all required fields must be present and non-empty
    required_fields = ["asset", "threat", "control", "residual_risk"]
    for field in required_fields:
        val = scenario.get(field)
        if not val or not str(val).strip():
            return {
                "status": "FAIL",
                "missing_field": field,
                "message": f"Scenario fails rubric: Missing required field '{field}'."
            }

    asset = str(scenario["asset"]).strip()
    threat = str(scenario["threat"]).strip().lower()
    control = str(scenario["control"]).strip().lower()
    residual = str(scenario["residual_risk"]).strip()

    # 2. Control relevance check:
    # If control only mentions physical security keywords while threat is software/network infrastructure
    is_physical_control = any(k in control for k in PHYSICAL_SECURITY_KEYWORDS)
    is_cyber_threat = any(k in threat for k in ["vulnerability", "buffer overflow", "rce", "exploit", "unpatched", "malware"])
    
    if is_physical_control and is_cyber_threat:
        return {
            "status": "FLAGGED_FOR_REVIEW",
            "message": "Flagged for review: Control appears unrelated to the infrastructure threat."
        }

    return {
        "status": "PASS",
        "message": "Scenario is complete and internally consistent."
    }

def get_fictional_scenarios():
    """
    Returns three fictional scenarios tied to 6.3 End of module quiz / Infrastructure Security.
    """
    return {
        "normal": {
            "asset": "Production Kubernetes Container Cluster",
            "threat": "Unpatched container runtime vulnerability allowing container breakout",
            "control": "Automated vulnerability scanning and monthly rolling OS and node patching",
            "residual_risk": "Zero-day vulnerability window before security patch publication"
        },
        "missing_asset": {
            "asset": "",  # Missing asset
            "threat": "Unauthorized SSH brute-force attack against Linux host",
            "control": "Disable password authentication and enforce bastion host with MFA",
            "residual_risk": "Compromise of engineer bastion credentials"
        },
        "unrelated_control": {
            "asset": "Payment Processing Database Host",
            "threat": "Remote buffer overflow vulnerability in unpatched web service",
            "control": "Physical security turnstiles and visitor badge requirements",
            "residual_risk": "Physical tailgating through headquarters gate"
        }
    }

def main():
    parser = argparse.ArgumentParser(description="Infrastructure Security Rubric Checker")
    parser.add_argument("--scenario", choices=["normal", "missing_asset", "unrelated_control", "all"], default="all",
                        help="Scenario to evaluate")
    args = parser.parse_args()

    scenarios = get_fictional_scenarios()
    if args.scenario == "all":
        results = {}
        for name, sc in scenarios.items():
            results[name] = check_scenario(sc)
        print(json.dumps(results, indent=2))
    else:
        sc = scenarios[args.scenario]
        res = check_scenario(sc)
        print(json.dumps(res, indent=2))

if __name__ == "__main__":
    main()
