"""Bounded Conversation Memory with Invariant Verification and State Trace (R34-T053).

Extends 2.1 IAM key concepts.
Demonstrates session memory bounds and defensiveness:
- Retains at most three conversation records in arrival order (FIFO).
- Adding A, B, C, D retains B, C, D.
- Exposes a defensive copy so mutating returned records cannot alter stored memory.
- Records intermediate state trace after each operation to verify invariants.
"""

from __future__ import annotations

import argparse
import copy
import sys
from typing import Any, Dict, List, Optional


class BoundedConversationMemory:
    """Stores at most `capacity` conversation records in arrival order."""

    def __init__(self, capacity: int = 3) -> None:
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        self._capacity = capacity
        self._records: List[Dict[str, Any]] = []
        self._trace: List[Dict[str, Any]] = []
        self._record_trace("INIT")

    @property
    def capacity(self) -> int:
        return self._capacity

    def add_record(self, record: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Append a record, evicting the oldest if capacity is exceeded.

        Returns a defensive copy of the updated records list.
        """
        # Store a deepcopy to prevent caller mutations from affecting internal state
        stored_entry = copy.deepcopy(record)
        self._records.append(stored_entry)
        if len(self._records) > self._capacity:
            self._records.pop(0)

        self._record_trace(f"ADD_{record.get('id', 'RECORD')}")
        return self.get_records()

    def get_records(self) -> List[Dict[str, Any]]:
        """Return a defensive deepcopy of stored records."""
        return copy.deepcopy(self._records)

    def get_trace(self) -> List[Dict[str, Any]]:
        """Return a defensive copy of the intermediate state trace."""
        return copy.deepcopy(self._trace)

    def _record_trace(self, action: str) -> None:
        state_snapshot = {
            "step": len(self._trace),
            "action": action,
            "count": len(self._records),
            "records": copy.deepcopy(self._records),
            "ids": [r.get("id") for r in self._records],
        }
        self._trace.append(state_snapshot)


def run_demonstration(scenario: str) -> int:
    print(f"Scenario: {scenario}")

    if scenario == "normal":
        memory = BoundedConversationMemory(capacity=3)
        records = [
            {"id": "A", "speaker": "user", "message": "Login request"},
            {"id": "B", "speaker": "system", "message": "Challenge issued"},
            {"id": "C", "speaker": "user", "message": "MFA response verified"},
            {"id": "D", "speaker": "system", "message": "Session token granted"},
        ]

        print("Adding records A, B, C, D to bounded memory (capacity 3)...")
        for r in records:
            current = memory.add_record(r)
            ids = [x["id"] for x in current]
            print(f"Added {r['id']} -> Stored IDs: {ids}")

        # Check invariant 1: Exactly retains B, C, D
        final_records = memory.get_records()
        final_ids = [x["id"] for x in final_records]
        print(f"Final stored records (arrival order): {final_ids}")
        assert final_ids == ["B", "C", "D"], f"Expected ['B', 'C', 'D'], got {final_ids}"

        # Check invariant 2: Mutation of returned list does not alter memory
        tampered = memory.get_records()
        tampered.append({"id": "E", "message": "Malicious injected record"})
        tampered[0]["id"] = "TAMPERED"

        verified = memory.get_records()
        verified_ids = [x["id"] for x in verified]
        print(f"Verified stored records after caller mutation attempt: {verified_ids}")
        assert verified_ids == ["B", "C", "D"], "Immutability invariant failed!"
        assert verified[0]["id"] == "B", "Internal record was mutated!"

        # Print intermediate state trace
        print("\nIntermediate State Trace:")
        for t in memory.get_trace():
            print(f"  Step {t['step']} [{t['action']}]: {t['ids']}")

        return 0

    elif scenario == "boundary":
        # Boundary case: Add fewer than capacity (e.g. 1 or 2 records)
        memory = BoundedConversationMemory(capacity=3)
        memory.add_record({"id": "A", "message": "Initial hello"})
        stored = memory.get_records()
        print(f"Boundary (count < capacity): {[r['id'] for r in stored]}")
        assert len(stored) == 1
        assert stored[0]["id"] == "A"
        return 0

    elif scenario == "failure":
        # Failure case: Simulate invariant check failure and exit non-zero
        memory = BoundedConversationMemory(capacity=3)
        for r in [{"id": "A"}, {"id": "B"}, {"id": "C"}, {"id": "D"}]:
            memory.add_record(r)
        stored_ids = [r["id"] for r in memory.get_records()]
        print("Failure simulation check: Asserting incorrect retention of 'A'...", file=sys.stderr)
        try:
            assert "A" in stored_ids, "Expected 'A' to be evicted from bounded memory"
            return 0
        except AssertionError as err:
            print(f"Expected failure caught: {err}", file=sys.stderr)
            return 1

    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Bounded Conversation Memory Example")
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
