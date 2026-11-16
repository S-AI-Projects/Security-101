import json
from pathlib import Path


REQUIRED_FIELDS = ("asset", "threat", "control", "residual_risk")
QUESTION_BANK = {
    "Q1": {
        "prompt": "After vulnerabilities are assessed and prioritized, what comes next in the vulnerability management process?",
        "options": {
            "A": "Continuous monitoring",
            "B": "Mitigation",
            "C": "Identification",
        },
        "answer": "B",
        "rationale": "Mitigation follows prioritization. Verification then checks whether the mitigation worked.",
    },
    "Q2": {
        "prompt": "Which task is a core CSPM capability?",
        "options": {
            "A": "Scanning cloud resources for insecure configurations",
            "B": "Replacing all application security testing",
            "C": "Guaranteeing that no cloud incident can occur",
        },
        "answer": "A",
        "rationale": "CSPM assesses cloud configurations, identifies misconfigurations and policy deviations, and supports monitoring and reporting.",
    },
    "Q3": {
        "prompt": "What best describes a CNAPP?",
        "options": {
            "A": "An integrated platform combining cloud-native security capabilities across the application lifecycle",
            "B": "A vulnerability score used to rank software defects",
            "C": "A tool used only to scan network ports",
        },
        "answer": "A",
        "rationale": "A CNAPP brings together cloud and application security capabilities, such as CSPM, container and infrastructure-as-code scanning, and workload protection.",
    },
}


def check_scenario(scenario):
    if not isinstance(scenario, dict):
        return {
            "status": "FAIL",
            "errors": ["Scenario must be a JSON object."],
            "warnings": [],
        }

    errors = []
    for field in REQUIRED_FIELDS:
        value = scenario.get(field)
        if not isinstance(value, str) or not value.strip():
            errors.append(f"Missing or invalid required field: {field}")

    if errors:
        return {"status": "FAIL", "errors": errors, "warnings": []}

    if scenario.get("control_matches_threat") is not True:
        if scenario.get("control_matches_threat") is False:
            warning = "The control may not address the stated threat; human review is required."
        else:
            warning = "Control-to-threat fit is not explicitly confirmed; human review is required."
        return {"status": "REVIEW", "errors": [], "warnings": [warning]}

    return {"status": "PASS", "errors": [], "warnings": []}


def check_answer(question_id, selected_option):
    question = QUESTION_BANK.get(question_id)
    if question is None:
        return {"status": "FAIL", "rationale": "Unknown question ID."}

    if not isinstance(selected_option, str):
        return {"status": "FAIL", "rationale": question["rationale"]}

    normalized_option = selected_option.strip().upper()
    if normalized_option not in question["options"]:
        return {"status": "FAIL", "rationale": question["rationale"]}

    status = "PASS" if normalized_option == question["answer"] else "FAIL"
    return {"status": status, "rationale": question["rationale"]}


def run_example():
    fixture_path = Path(__file__).with_name("fixtures.json")
    with fixture_path.open(encoding="utf-8") as fixture_file:
        fixtures = json.load(fixture_file)

    scenario_results = []
    for scenario in fixtures["scenarios"]:
        result = check_scenario(scenario)
        scenario_results.append(
            {"name": scenario["name"], "status": result["status"]}
        )

    question_results = []
    for question_id in QUESTION_BANK:
        result = check_answer(question_id, fixtures["answers"].get(question_id))
        question_results.append({"id": question_id, "status": result["status"]})

    statuses = [result["status"] for result in scenario_results + question_results]
    summary = {status: statuses.count(status) for status in ("PASS", "REVIEW", "FAIL")}
    return {
        "scenarios": scenario_results,
        "questions": question_results,
        "summary": summary,
    }


if __name__ == "__main__":
    print(json.dumps(run_example(), indent=2))