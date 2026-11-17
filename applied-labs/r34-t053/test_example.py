"""Unit tests for Bounded Conversation Memory (R34-T053)."""

import unittest
from example import BoundedConversationMemory


class TestBoundedConversationMemory(unittest.TestCase):
    def test_retains_at_most_three_in_arrival_order(self):
        mem = BoundedConversationMemory(capacity=3)
        mem.add_record({"id": "A", "val": 1})
        mem.add_record({"id": "B", "val": 2})
        mem.add_record({"id": "C", "val": 3})
        self.assertEqual([r["id"] for r in mem.get_records()], ["A", "B", "C"])

        # Adding fourth record evicts oldest 'A' and retains 'B', 'C', 'D'
        mem.add_record({"id": "D", "val": 4})
        self.assertEqual([r["id"] for r in mem.get_records()], ["B", "C", "D"])

    def test_caller_mutation_does_not_alter_stored_memory(self):
        mem = BoundedConversationMemory(capacity=3)
        mem.add_record({"id": "A", "data": "original"})
        records = mem.get_records()
        records.append({"id": "INJECTED"})
        records[0]["data"] = "MODIFIED"

        fresh_records = mem.get_records()
        self.assertEqual(len(fresh_records), 1)
        self.assertEqual(fresh_records[0]["data"], "original")
        self.assertEqual(fresh_records[0]["id"], "A")

    def test_input_record_mutation_after_add(self):
        mem = BoundedConversationMemory(capacity=3)
        input_record = {"id": "A", "val": "initial"}
        mem.add_record(input_record)
        # Mutate local dict after passing it
        input_record["val"] = "mutated_externally"

        stored = mem.get_records()
        self.assertEqual(stored[0]["val"], "initial")

    def test_state_trace_invariants(self):
        mem = BoundedConversationMemory(capacity=3)
        mem.add_record({"id": "A"})
        mem.add_record({"id": "B"})
        mem.add_record({"id": "C"})
        mem.add_record({"id": "D"})

        trace = mem.get_trace()
        # Init + 4 adds = 5 trace snapshots
        self.assertEqual(len(trace), 5)
        self.assertEqual(trace[0]["ids"], [])
        self.assertEqual(trace[1]["ids"], ["A"])
        self.assertEqual(trace[2]["ids"], ["A", "B"])
        self.assertEqual(trace[3]["ids"], ["A", "B", "C"])
        self.assertEqual(trace[4]["ids"], ["B", "C", "D"])

        # Invariant: count never exceeds capacity
        for t in trace:
            self.assertLessEqual(t["count"], 3)

    def test_boundary_empty_and_single_entry(self):
        mem = BoundedConversationMemory(capacity=3)
        self.assertEqual(mem.get_records(), [])
        mem.add_record({"id": "ONLY"})
        self.assertEqual(len(mem.get_records()), 1)


if __name__ == "__main__":
    unittest.main()
