# Typed Tool Dispatch with Allowlist and Validation (R34-T057)

This applied lab extends **8.2 AI security capabilities** by implementing a secure tool dispatch contract.

## Overview

In agentic and AI-assisted workflows, language models invoke external capabilities via tool calling. Exposing tools without boundary checks creates significant vulnerabilities, including prompt injection leading to remote code execution, type-confusion errors, and unwanted secondary tool chaining.

This lab implements an explicit local dispatch security policy:
1. **Explicit Allowlist**: Only tools present in `{"add", "multiply"}` are permitted.
2. **Schema & Numeric Type Validation**: Arguments `a` and `b` must be numeric (`int` or `float`). Strings, booleans, and missing fields are rejected with structured errors.
3. **Execution Gating**: A failed call aborts immediately and cannot trigger fallbacks or execute another tool.

## Applied Scenario Assessment Questions

1. **Predict an Output**:
   - *Question*: What is the output of dispatching `add(2, 3)`?
   - *Answer*: `{"status": "SUCCESS", "tool": "add", "result": 5}`.
   - *Rationale*: Tool is allowlisted and both parameters are valid integers. Tested in `test_question_1_predict_output`.
2. **Diagnose a Failure**:
   - *Question*: Why does dispatching `multiply("2", 3)` fail?
   - *Answer*: Returns `{"status": "ERROR", "error_type": "INVALID_ARGUMENT"}`.
   - *Rationale*: The string argument `"2"` violates numeric schema requirements and is rejected prior to dispatch. Tested in `test_question_2_diagnose_failure`.
3. **Choose a Boundary Policy**:
   - *Question*: What boundary policy governs an unlisted tool call (e.g. `system_exec`)?
   - *Answer*: Returns `{"status": "ERROR", "error_type": "UNKNOWN_TOOL"}`.
   - *Rationale*: Strict default-deny allowlist rejects unknown tools before invocation. Tested in `test_question_3_choose_boundary_policy`.

## Invocation

```bash
python3 ./applied-labs/r34-t057/example.py
python3 ./applied-labs/r34-t057/example.py --scenario boundary
python3 ./applied-labs/r34-t057/example.py --scenario failure
```

## Running Tests

```bash
python3 -m unittest discover -s ./applied-labs/r34-t057 -p "test_*.py"
```

## Scope and Limitations

This is a local contract fixture using Python standard library primitives. It does not implement Model Context Protocol (MCP) transport (such as JSON-RPC over stdio/SSE) or call external LLM providers.
