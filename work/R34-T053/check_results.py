"""Assertion checks for R34-T053 bounded conversation memory."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "applied-labs/r34-t053"))

from example import BoundedConversationMemory


def main() -> int:
    mem = BoundedConversationMemory(capacity=3)
    for r in [{"id": "A"}, {"id": "B"}, {"id": "C"}, {"id": "D"}]:
        mem.add_record(r)

    stored = mem.get_records()
    stored_ids = [x["id"] for x in stored]
    assert stored_ids == ["B", "C", "D"], f"Expected ['B', 'C', 'D'], got {stored_ids}"

    # Mutability check
    stored.append({"id": "E"})
    stored[0]["id"] = "TAMPERED"
    fresh = mem.get_records()
    assert [x["id"] for x in fresh] == ["B", "C", "D"], "Memory was mutated by caller!"

    # Invariant trace check
    trace = mem.get_trace()
    assert len(trace) == 5, f"Expected 5 trace steps, got {len(trace)}"
    assert trace[-1]["ids"] == ["B", "C", "D"]

    if "--deliberate-wrong-result" in sys.argv:
        # Deliberately assert 'A' was retained
        assert "A" in stored_ids, "Deliberate wrong result check"

    print("All R34-T053 checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
