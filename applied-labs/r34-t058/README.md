# Network Range Classification and Error Recovery (R34-T058)

This applied lab extends **3.1 Networking key concepts** by classifying sample IP addresses against an allowlisted CIDR range using Python's standard `ipaddress` library without performing any network scanning.

## Overview

In firewall rule configuration, access control lists (ACLs), and Zero Trust networking, systems classify inbound and outbound packets based on CIDR subnet membership.

### Classification Logic

- **Allowlisted CIDR**: `192.0.2.0/24`
- `192.0.2.1` -> Belongs to `192.0.2.0/24` -> `[ALLOW]`
- `198.51.100.1` -> External address outside subnet -> `[DENY]`
- Malformed strings (e.g. `999.999.999.999`) or missing data -> `[ERROR]`

### Error Handling and Graceful Recovery

When evaluating batches or streaming inputs, malformed or missing IP records trigger structured errors (`MALFORMED_IP` or `MISSING_DATA`) without throwing uncaught exceptions or polluting state. The processor continues immediately to the next input, demonstrating robust recovery.

## Invocation

```bash
python3 ./applied-labs/r34-t058/example.py
python3 ./applied-labs/r34-t058/example.py --scenario boundary
python3 ./applied-labs/r34-t058/example.py --scenario failure
```

## Running Tests

```bash
python3 -m unittest discover -s ./applied-labs/r34-t058 -p "test_*.py"
```

## Scope and Limitations

This script uses Python's standard `ipaddress` library to perform pure in-memory subnet containment checks. It performs **no** live packet sniffing, ICMP pinging, port scanning, or socket connections.
