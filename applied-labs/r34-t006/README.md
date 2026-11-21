# AI Tool Allowlist Policy Validator (R34-T006)

Extends **8.1 AI security key concepts** by demonstrating action policy validation:
- Explicit allowed-tool schema (`read_document` with required `path`).
- Blocks unauthorized tools (e.g. `delete_document`) and incomplete calls before dispatch.
- Demonstrates refactoring from monolithic dispatch to separated `PolicyValidator`.

## Running Tests
```bash
python3 -m unittest discover -s ./applied-labs/r34-t006 -p "test_*.py"
```
