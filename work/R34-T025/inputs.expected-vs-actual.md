# R34-T025 Verification Evidence

## Environment

- Python `3.9.6`
- Standard library only
- Command:
  `python3 -m unittest discover -s ./applied-labs/r34-t025 -p "test_*.py"`

## Canonical Fixture

- Input: address `192.0.2.1`, CIDR `192.0.2.0/24`
- Expected: `True`
- Actual: `True`
- Result: matched

## Outside Fixture

- Input: address `198.51.100.1`, CIDR `192.0.2.0/24`
- Expected: `False`
- Actual: `False`
- Result: matched

## Boundary Fixture

- `192.0.2.0` expected `True`, actual `True`
- `192.0.2.255` expected `True`, actual `True`
- `192.0.3.0` expected `False`, actual `False`

## Failure Fixture

- Input: `192.0.2.not-an-ip`
- Expected: `ValueError` with `Malformed IPv4 address`
- Actual: exit code `1` with `Malformed IPv4 address: '192.0.2.not-an-ip'`

## Baseline Equivalence

- Before: `baseline_address_allowed`
- After: `AddressAllowlist.contains`
- Fixture: canonical, outside, network, and broadcast addresses
- Expected: identical result dictionaries
- Actual: `baseline_extracted_equivalent=true`

## Regression Suite

- Expected: 13 tests run, zero failures
- Actual: `Ran 13 tests in 0.001s`, `OK`
