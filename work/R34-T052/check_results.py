"""Assertion checks and evidence validation for R34-T052."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "applied-labs/r34-t052"))

from example import (
    CapabilityNotNegotiatedError,
    dispatch_capability,
    negotiate_capabilities,
    safe_dispatch,
)


def main() -> int:
    client = {"tools", "resources"}
    server = {"tools", "prompts"}
    negotiated = negotiate_capabilities(client, server)
    assert negotiated == {"tools"}, f"Expected {{'tools'}}, got {negotiated}"

    # Negotiated capability succeeds
    res = dispatch_capability(negotiated, "tools")
    assert res["status"] == "SUCCESS"

    # Unnegotiated capability rejected
    status, rejected_res = safe_dispatch(negotiated, "resources")
    assert status == "REJECTED"
    assert "not negotiated" in rejected_res["error"]

    # Boundary case: disjoint sets
    empty_neg = negotiate_capabilities({"resources"}, {"prompts"})
    assert empty_neg == set()
    b_status, b_res = safe_dispatch(empty_neg, "resources")
    assert b_status == "REJECTED"

    # Deliberate wrong check
    if "--deliberate-wrong-result" in sys.argv:
        # Deliberately assert that unnegotiated 'resources' was in negotiated
        assert "resources" in negotiated, "Deliberate wrong result check"

    print("All R34-T052 checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
