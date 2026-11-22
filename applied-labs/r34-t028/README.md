# Network Range Classification & Error Recovery (R34-T028)

This applied lab extends **[3.3 Network security capabilities.md](../../3.3%20Network%20security%20capabilities.md)** by implementing an offline CIDR subnet classifier using Python's standard `ipaddress` library without performing any network scanning.

## Overview

In traditional firewalls and cloud network security groups (NSGs), packet filtering begins with IP address classification against predefined CIDR blocks. Robust network security systems must:
1. **Accurately Classify Containment**: Determine whether an IPv4/IPv6 address falls within an authorized CIDR block.
2. **Handle Malformed Inputs**: Catch invalid or missing data gracefully without throwing unhandled exceptions or corrupting state.
3. **Recover Gracefully**: Immediately resume processing subsequent valid packets or logs after encountering an error.

## Key Contract Requirements

- `192.0.2.1` belongs to `192.0.2.0/24` -> `[ALLOW]` (`is_member=True`).
- `198.51.100.1` does not belong to `192.0.2.0/24` -> `[DENY]` (`is_member=False`).
- Malformed inputs (e.g. `invalid-ip-string`, `999.999.999.999`) are rejected with structured `MALFORMED_IP` errors.
- Missing data (empty strings, `None`) is rejected with structured `MISSING_DATA` errors.
- **Contribution Focus**: Demonstrates error explanation on invalid inputs and subsequent recovery on the next valid address (`192.0.2.42` -> `[ALLOW]`).

## Prerequisites and Invocation

- **Prerequisites**: Python 3 standard library (`ipaddress`, `argparse`, `sys`). No external dependencies, cloud accounts, GPUs, or network scanning tools required.
- **Invocation**:

From the repository root:

```bash
# Run normal scenario (classification and recovery demonstration)
python3 ./applied-labs/r34-t028/example.py

# Run boundary scenario (network and broadcast boundary checks)
python3 ./applied-labs/r34-t028/example.py --scenario boundary

# Run failure scenario (rejects malformed CIDR definition with exit code 1)
python3 ./applied-labs/r34-t028/example.py --scenario failure

# Run specific single address check
python3 ./applied-labs/r34-t028/example.py --ip 192.0.2.1
```

## Expected Output (`--scenario normal`)

```text
Scenario: Illustrative network range classification based on "3.3 Network security capabilities.md"; educational mock CIDR checks, no network scanning.
Allowlisted Network: 192.0.2.0/24
[ALLOW] IP: 192.0.2.1 -> Belongs to 192.0.2.0/24
[DENY]  IP: 198.51.100.1 -> Outside 192.0.2.0/24
[ERROR] IP: invalid-ip-string -> MALFORMED_IP: Malformed input: 'invalid-ip-string' is not a valid IPv4 or IPv6 address ('invalid-ip-string' does not appear to be an IPv4 or IPv6 address).
[ERROR] IP: '' -> MISSING_DATA: Missing data: IP address string cannot be empty or None.
[ALLOW] IP: 192.0.2.42 -> Belongs to 192.0.2.0/24
Recovery: Following malformed/missing entries, subsequent valid address was processed successfully.
```

## Error Explanation and Recovery Focus

When processing sequential packet headers or firewall access logs, encountering an invalid address format (`invalid-ip-string`) or missing field (`""`) yields a structured error description without aborting the program. The classifier immediately recovers and classifies the next valid record (`192.0.2.42`) as `ALLOW`.

## Running the Automated Test Suite

Run unit tests via unittest discovery:

```bash
python3 -m unittest discover -s ./applied-labs/r34-t028 -p "test_*.py" -v
```

Expected result: 12 tests passing with zero failures.

## Scope and Limitations

This implementation is a local, deterministic Python simulation using standard library `ipaddress` parsing. It performs purely in-memory IP calculations and does **not** perform active network probing, ICMP pings, port scanning, or physical firewall hardware configuration.
