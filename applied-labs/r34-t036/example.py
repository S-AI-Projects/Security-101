import json
from pathlib import Path

FIXTURE = Path(__file__).with_name("scenarios.json")

LABELS = {
    "unauthorized_reading": "confidentiality",
    "altered_records": "integrity",
    "service_unavailable": "availability",
}

def classify(scenario):
    return [
        label for impact, label in LABELS.items()
        if scenario.get(impact, False)
    ]

def main():
    scenarios = json.loads(FIXTURE.read_text())
    results = [
        {"id": item["id"], "labels": classify(item["impacts"])}
        for item in scenarios
    ]
    print(json.dumps(results, indent=2))

if __name__ == "__main__":
    main()
