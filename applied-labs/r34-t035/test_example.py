
import unittest
from example import (
    baseline_negotiate,
    negotiate,
    dispatch,
)


class TestCapabilityNegotiation(unittest.TestCase):

    def setUp(self):
        self.client = {
            "tools": True,
            "resources": True,
        }

        self.server = {
            "tools": True,
            "prompts": True,
        }

    def test_only_tools_are_negotiated(self):
        self.assertEqual(negotiate(self.client, self.server), {"tools"})

    def test_baseline_and_refactored_are_equivalent(self):
        self.assertEqual(
            baseline_negotiate(self.client, self.server),
            negotiate(self.client, self.server),
        )

    def test_tools_are_dispatched(self):
        dispatch_log = []

        result = dispatch("tools", negotiate(self.client, self.server), dispatch_log)

        self.assertEqual(result, "tools dispatched")
        self.assertEqual(dispatch_log, ["tools"])

    def test_resources_rejected_before_dispatch(self):
        dispatch_log = []

        with self.assertRaises(PermissionError):
            dispatch(
                "resources",
                negotiate(self.client, self.server),
                dispatch_log,
            )

        self.assertEqual(dispatch_log, [])

    def test_empty_intersection(self):
        client = {"resources": True}
        server = {"prompts": True}

        self.assertEqual(negotiate(client, server), set())


if __name__ == "__main__":
    unittest.main()
