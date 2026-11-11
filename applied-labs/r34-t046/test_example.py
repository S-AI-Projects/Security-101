import unittest
from unittest.mock import Mock

from example import CLIENT, SERVER, dispatch, mock_handler, negotiate


def baseline_dispatch(client, server, capability, handle):
    """Original version with the intersection inside dispatch."""
    common = {name for name in client if name in server}
    if capability not in common:
        return "REJECTED (unnegotiated capability)"
    return handle(capability)


class CapabilityTests(unittest.TestCase):
    def test_required_intersection(self):
        self.assertEqual(negotiate(CLIENT, SERVER), {"tools"})

    def test_only_negotiated_capability_dispatches(self):
        handle = Mock(side_effect=mock_handler)
        self.assertEqual(dispatch(CLIENT, SERVER, "tools", handle),
                         "ACCEPTED (mock tools handler)")
        self.assertEqual(dispatch(CLIENT, SERVER, "resources", handle),
                         "REJECTED (unnegotiated capability)")
        handle.assert_called_once_with("tools")

    def test_empty_overlap_rejects_all_requests(self):
        server = frozenset({"prompts"})
        handle = Mock()
        self.assertEqual(negotiate(CLIENT, server), set())
        self.assertEqual(dispatch(CLIENT, server, "tools", handle),
                         "REJECTED (unnegotiated capability)")
        handle.assert_not_called()

    def test_baseline_and_refactor_match(self):
        for client, server in ((CLIENT, SERVER), (CLIENT, CLIENT), (CLIENT, frozenset())):
            for capability in ("tools", "resources", "prompts"):
                with self.subTest(client=client, server=server, capability=capability):
                    before = Mock(side_effect=mock_handler)
                    after = Mock(side_effect=mock_handler)
                    self.assertEqual(
                        dispatch(client, server, capability, after),
                        baseline_dispatch(client, server, capability, before),
                    )
                    self.assertEqual(after.call_args_list, before.call_args_list)
