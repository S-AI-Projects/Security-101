"""Assertion checks for R34-T058 network range classification."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "applied-labs/r34-t058"))

from example import classify_ip, process_ip_sequence


def main() -> int:
    net = "192.0.2.0/24"
    r1 = classify_ip("192.0.2.1", net)
    assert r1["status"] == "ALLOW"
    assert r1["is_member"] is True

    r2 = classify_ip("198.51.100.1", net)
    assert r2["status"] == "DENY"
    assert r2["is_member"] is False

    r3 = classify_ip("999.999.999.999", net)
    assert r3["status"] == "ERROR"
    assert r3["error_type"] == "MALFORMED_IP"

    # Recovery check
    seq_res = process_ip_sequence(["192.0.2.1", "bad_ip", "192.0.2.5"], net)
    assert seq_res[0]["status"] == "ALLOW"
    assert seq_res[1]["status"] == "ERROR"
    assert seq_res[2]["status"] == "ALLOW"

    if "--deliberate-wrong-result" in sys.argv:
        assert r2["status"] == "ALLOW", "Deliberate wrong result check"

    print("All R34-T058 checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
