"""
Data Security Scenario Rubric Checker with Offline Service Adapter (Task R34-T005)
Evaluates Module 7 data security scenarios via a callable adapter interface.
"""
import sys
import json
import argparse

PHYSICAL_SECURITY_KEYWORDS = ["shredder", "fence", "turnstile", "badge", "patrol", "door", "guard"]
DATA_THREAT_KEYWORDS = ["exfiltration", "sql injection", "unencrypted", "leakage", "breach", "plaintext"]

class DataSecurityEvaluatorInterface:
    """Callable interface definition for scenario evaluation."""
    def evaluate(self, scenario):
        raise NotImplementedError

class LocalOfflineSecurityAdapter(DataSecurityEvaluatorInterface):
    """
    Deterministic offline adapter for evaluating data security scenarios.
    Mock behavior: Replaces real remote policy services with local rule verification.
    """
    def evaluate(self, scenario):
        if not isinstance(scenario, dict):
            return {"status": "FAIL", "message": "Scenario must be a dictionary."}

        required_fields = ["asset", "threat", "control", "residual_risk"]
        for field in required_fields:
            val = scenario.get(field)
            if not val or not str(val).strip():
                return {
                    "status": "FAIL",
                    "missing_field": field,
                    "message": f"Scenario fails rubric: Missing required field '{field}'."
                }

        threat = str(scenario["threat"]).lower()
        control = str(scenario["control"]).lower()

        # Flag if physical control is proposed for digital data threat
        is_physical_control = any(k in control for k in PHYSICAL_SECURITY_KEYWORDS)
        is_digital_threat = any(k in threat for k in DATA_THREAT_KEYWORDS)

        if is_physical_control and is_digital_threat:
            return {
                "status": "FLAGGED_FOR_REVIEW",
                "message": "Flagged for review: Control is physical but threat is digital data exfiltration."
            }

        return {
            "status": "PASS",
            "message": "Scenario is complete and internally consistent."
        }

def get_fictional_scenarios():
    return {
        "normal": {
            "asset": "Customer Credit Card & Financial Records",
            "threat": "Data exfiltration via unencrypted public API query",
            "control": "TLS 1.3 transit encryption, AES-256 field encryption, and tokenized API auth",
            "residual_risk": "Compromised administrative credentials accessing key vault"
        },
        "missing_asset": {
            "asset": "",
            "threat": "Unauthorized database backup exfiltration",
            "control": "Database transparent data encryption and export auditing",
            "residual_risk": "Insider theft of encryption keys"
        },
        "unrelated_control": {
            "asset": "Patient Medical History Database",
            "threat": "SQL injection exfiltrating plaintext patient records",
            "control": "Paper shredder disposal policy in corporate mailroom",
            "residual_risk": "Improper physical document shredding"
        }
    }

def main():
    parser = argparse.ArgumentParser(description="Data Security Scenario Rubric Checker")
    parser.add_argument("--scenario", choices=["normal", "missing_asset", "unrelated_control", "all"], default="all")
    args = parser.parse_args()

    adapter = LocalOfflineSecurityAdapter()
    scenarios = get_fictional_scenarios()

    if args.scenario == "all":
        results = {name: adapter.evaluate(sc) for name, sc in scenarios.items()}
        print(json.dumps(results, indent=2))
    else:
        res = adapter.evaluate(scenarios[args.scenario])
        print(json.dumps(res, indent=2))

if __name__ == "__main__":
    main()
