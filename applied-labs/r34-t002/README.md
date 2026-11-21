# IAM Access Policy Evaluator (R34-T002)

This applied lab extends **2.3 IAM capabilities** by demonstrating role-based access policy evaluation using:
- **Default Deny**: Any action/resource not explicitly permitted is blocked.
- **Deny Overrides Allow**: If conflicting rules exist for the same subject and resource, DENY takes precedence.

## Key Test Cases
1. `reader` may read `public` (`ALLOW`).
2. `reader` cannot write `public` (`DENY`).
3. Explicit `DENY` overrides matching `ALLOW` (`DENY`).
4. Unknown role is denied (`DENY`).

## Usage
```bash
python3 applied-labs/r34-t002/example.py --role reader --action read --resource public
python3 applied-labs/r34-t002/example.py --role reader --action write --resource public
```

## Running Unit Tests
```bash
python3 -m unittest discover -s ./applied-labs/r34-t002 -p "test_*.py"
```
