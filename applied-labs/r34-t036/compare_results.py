import json
import sys
from pathlib import Path

expected = json.loads(Path("work/R34-T036/expected.json").read_text())
actual = json.loads(Path("work/R34-T036/actual.json").read_text())

if expected != actual:
    print("RESULT: MISMATCH")
    sys.exit(1)

print("RESULT: MATCH")
