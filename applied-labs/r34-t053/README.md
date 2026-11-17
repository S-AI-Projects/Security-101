# Bounded Conversation Memory with Invariant Verification (R34-T053)

This applied lab extends **2.1 IAM key concepts** by demonstrating session boundaries, FIFO memory retention, and immutable state exposure.

## Overview

In secure IAM and authentication systems, sessions maintain bounded state to limit resource exposure and enforce freshness. This lab implements a bounded conversation memory buffer that:
- Holds at most 3 conversation records in strict arrival order (FIFO).
- Automatically evicts the oldest record when capacity is exceeded (adding A, B, C, D retains B, C, D).
- Provides defensive copies so callers cannot alter internal state by mutating returned structures.
- Records an explicit intermediate state trace after each operation to enable invariant verification.

## Invocation

Run from the repository root:

```bash
python3 ./applied-labs/r34-t053/example.py
python3 ./applied-labs/r34-t053/example.py --scenario boundary
python3 ./applied-labs/r34-t053/example.py --scenario failure
```

## Running Tests

```bash
python3 -m unittest discover -s ./applied-labs/r34-t053 -p "test_*.py"
```

## Scope and Limitations

This implementation is a local, in-memory Python structure illustrating defensive state handling and session limits. It does not interface with persistent session databases, distributed caches (e.g. Redis), or hardware security modules.
