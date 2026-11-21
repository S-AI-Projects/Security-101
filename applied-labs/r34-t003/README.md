# SecOps Typed Tool Dispatcher (R34-T003)

This applied lab extends **4.3 SecOps capabilities** by demonstrating secure tool dispatching:
- Explicit allowlist filtering (`add`, `multiply`).
- Strict argument type checking (numbers only).
- Structured error handling preventing cascade or execution of unauthorized tools.

## Key Test Cases
1. `add(2, 3)` -> `5`
2. `multiply(2, 3)` -> `6`
3. Unknown tool -> Structured error (`UNKNOWN_TOOL`)
4. String argument -> Structured error (`INVALID_ARGUMENT`)

## Running Unit Tests
```bash
python3 -m unittest discover -s ./applied-labs/r34-t003 -p "test_*.py"
```
