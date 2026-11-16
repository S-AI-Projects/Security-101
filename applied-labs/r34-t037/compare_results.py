import json
from pathlib import Path

evidence = Path("work/R34-T037")
expected = [json.loads(line) for line in (evidence / "expected.jsonl").read_text().splitlines()]
actual = [json.loads(line) for line in (evidence / "actual.jsonl").read_text().splitlines()]

if expected != actual:
    print("RESULT: MISMATCH")
    raise SystemExit(1)

print("RESULT: MATCH")
