# Responsible AI Allowlisted Action Policy (R34-T010)

Extends **8.3 Responsible AI** by enforcing pre-execution allowlists and schema validation for AI tools:
- Allowed `read` with valid path passes.
- Unknown `delete` tool and missing required arguments are rejected before reaching executor.
- Includes Scenario Assessment questions covering output prediction, failure diagnosis, and boundary policy choice.

## Running Tests
```bash
python3 -m unittest discover -s ./applied-labs/r34-t010 -p "test_*.py"
```
