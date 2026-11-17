"""Infrastructure Security Scenario Rubric Checker with Evaluation Experiment (R34-T059).

Extends 6.3 End of module quiz.
Evaluates infrastructure security scenarios using a structural rubric checker.
Compares three small controlled configurations/input sizes (N=1, N=3, N=6)
evaluating correctness rate and processing throughput trade-offs without claiming model accuracy.
"""

from __future__ import annotations

import argparse
import sys
import time
from typing import Any, Dict, List, Optional, Tuple

REQUIRED_FIELDS = ("asset", "threat", "control", "residual_risk")

THREAT_CONTROL_KEYWORDS = {
    "unauthorized remote": ["rbac", "mtls", "tls", "authentication", "iam"],
    "eavesdropping": ["encryption", "mtls", "tls", "ipsec", "vpn", "service mesh"],
    "ddos": ["rate limit", "anycast", "waf", "scrubbing", "traffic shaping", "cdn"],
    "privilege escalation": ["least privilege", "rbac", "hardening", "monitoring"],
}


def check_scenario(scenario: Dict[str, Optional[str]]) -> Tuple[str, str]:
    """Check an infrastructure scenario against structural completeness and relevance."""
    for field in REQUIRED_FIELDS:
        val = scenario.get(field)
        if val is None or not str(val).strip():
            return "FAIL", f"Missing required field: {field}"

    threat = str(scenario["threat"]).strip().lower()
    control = str(scenario["control"]).strip().lower()

    matched_threat_key = None
    for threat_key in THREAT_CONTROL_KEYWORDS:
        if threat_key in threat:
            matched_threat_key = threat_key
            break

    if matched_threat_key:
        expected_keywords = THREAT_CONTROL_KEYWORDS[matched_threat_key]
        has_match = any(kw in control for kw in expected_keywords)
        if not has_match:
            return "FLAG_REVIEW", (
                f"Control '{scenario['control']}' appears unrelated to threat '{scenario['threat']}'; "
                "flagged for human review"
            )

    return "PASS", "Scenario meets structural rubric requirements"


def get_canonical_scenarios() -> List[Dict[str, Optional[str]]]:
    """Returns the three canonical infrastructure scenarios."""
    return [
        {
            "name": "Kubernetes API Server",
            "asset": "Production Kubernetes cluster API server",
            "threat": "Unauthorized remote administrative command execution",
            "control": "Enforce mutual TLS and strict role-based access control (RBAC)",
            "residual_risk": "Privilege escalation if an admin token is compromised",
            "expected_outcome": "PASS",
        },
        {
            "name": "Missing asset infra quiz scenario",
            "asset": "",
            "threat": "Eavesdropping on inter-pod overlay network traffic",
            "control": "Deploy service mesh with automatic mTLS encryption",
            "residual_risk": "Node-level compromise exposes pod memory",
            "expected_outcome": "FAIL",
        },
        {
            "name": "Mismatched infrastructure quiz control",
            "asset": "Bare-metal hypervisor fleet",
            "threat": "DDoS flooding against external API gateway",
            "control": "Implement BIOS password and disable USB boot in firmware",
            "residual_risk": "Firmware controls do not mitigate network-layer volumetric DDoS",
            "expected_outcome": "FLAG_REVIEW",
        },
    ]


def run_evaluation_experiment() -> Dict[str, Any]:
    """Compare three small controlled configurations/input sizes (N=1, N=3, N=6)."""
    canonical = get_canonical_scenarios()

    configurations = {
        "config_1_single": canonical[:1],
        "config_2_standard": canonical,
        "config_3_extended": canonical + canonical,
    }

    results = {}
    for cfg_name, items in configurations.items():
        count = len(items)
        correct_count = 0
        t0 = time.perf_counter()
        # Run iterations to obtain stable local timing
        iterations = 500
        for _ in range(iterations):
            for item in items:
                status, _ = check_scenario(item)
                if status == item["expected_outcome"]:
                    correct_count += 1
        elapsed = time.perf_counter() - t0

        total_evaluations = count * iterations
        correctness_rate = correct_count / total_evaluations
        avg_latency_us = (elapsed / total_evaluations) * 1_000_000

        results[cfg_name] = {
            "size": count,
            "total_evaluations": total_evaluations,
            "correctness_rate": round(correctness_rate, 4),
            "avg_latency_us": round(avg_latency_us, 2),
        }

    return results


def run_demonstration(scenario: str) -> int:
    print(f"Scenario mode: {scenario}")

    if scenario == "normal":
        scenarios = get_canonical_scenarios()
        for s in scenarios:
            status, msg = check_scenario(s)
            print(f"[{status}] {s['name']}: {msg}")
            assert status == s["expected_outcome"]

        print("\nEvaluation Experiment across 3 controlled configurations:")
        exp_results = run_evaluation_experiment()
        print(f"{'Configuration':<20} | {'Input Size':<10} | {'Correctness':<12} | {'Avg Latency (µs)':<16}")
        print("-" * 65)
        for name, data in exp_results.items():
            print(f"{name:<20} | {data['size']:<10} | {data['correctness_rate']*100:.1f}%{'':<6} | {data['avg_latency_us']:<16}")
        return 0

    elif scenario == "boundary":
        res = check_scenario({"asset": "", "threat": "", "control": "", "residual_risk": ""})
        print(f"Boundary all-empty check: {res}")
        assert res[0] == "FAIL"
        return 0

    elif scenario == "failure":
        print("Failure simulation check: Asserting invalid control passes...", file=sys.stderr)
        scenarios = get_canonical_scenarios()
        status, msg = check_scenario(scenarios[2])
        try:
            assert status == "PASS", "Expected mismatched control to be FLAG_REVIEW, not PASS"
            return 0
        except AssertionError as err:
            print(f"Expected failure caught: {err}", file=sys.stderr)
            return 1

    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Infrastructure Scenario Rubric Evaluation")
    parser.add_argument(
        "--scenario",
        choices=["normal", "boundary", "failure"],
        default="normal",
        help="Scenario mode to execute",
    )
    args = parser.parse_args()
    return run_demonstration(args.scenario)


if __name__ == "__main__":
    sys.exit(main())
