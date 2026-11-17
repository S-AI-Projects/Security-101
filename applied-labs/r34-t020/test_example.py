import unittest

from example import (
    AdapterError,
    LocalServiceAdapter,
    MatrixInputError,
    ServiceAdapterError,
    evaluate_responsibilities,
    load_matrix,
)


class TestResponsibilityMatrix(unittest.TestCase):
    def test_normal_scenario_returns_the_local_fixture(self):
        matrix = load_matrix(LocalServiceAdapter())

        self.assertEqual(len(matrix), 7)
        self.assertEqual(
            matrix[0],
            {
                "task": "Patch guest operating system",
                "service_model": "IaaS",
                "responsible_party": "customer",
            },
        )

    def test_iaas_paas_and_saas_are_supported(self):
        matrix = evaluate_responsibilities(
            [
                {"task": "IaaS task", "service_model": "IaaS", "responsible_party": "customer"},
                {"task": "PaaS task", "service_model": "PaaS", "responsible_party": "provider"},
                {"task": "SaaS task", "service_model": "SaaS", "responsible_party": "shared"},
            ]
        )

        self.assertEqual([row["service_model"] for row in matrix], ["IaaS", "PaaS", "SaaS"])
        self.assertEqual(
            [row["responsible_party"] for row in matrix],
            ["customer", "provider", "shared"],
        )

    def test_customer_ownership_is_preserved(self):
        matrix = evaluate_responsibilities(
            [{"task": "Manage guest OS", "service_model": "IaaS", "responsible_party": "customer"}]
        )

        self.assertEqual(matrix[0]["responsible_party"], "customer")

    def test_provider_ownership_is_preserved(self):
        matrix = evaluate_responsibilities(
            [{"task": "Maintain host", "service_model": "IaaS", "responsible_party": "provider"}]
        )

        self.assertEqual(matrix[0]["responsible_party"], "provider")

    def test_shared_ownership_is_preserved(self):
        matrix = evaluate_responsibilities(
            [{"task": "Review data use", "service_model": "PaaS", "responsible_party": "shared"}]
        )

        self.assertEqual(matrix[0]["responsible_party"], "shared")

    def test_missing_ownership_is_marked_unassigned(self):
        matrix = evaluate_responsibilities(
            [{"task": "Set access policy", "service_model": "SaaS"}]
        )

        self.assertEqual(matrix[0]["responsible_party"], "UNASSIGNED")

    def test_invalid_ownership_is_marked_invalid(self):
        for owner in ("unknown", None, ["customer"]):
            with self.subTest(owner=owner):
                matrix = evaluate_responsibilities(
                    [
                        {
                            "task": "Set access policy",
                            "service_model": "SaaS",
                            "responsible_party": owner,
                        }
                    ]
                )

                self.assertEqual(matrix[0]["responsible_party"], "INVALID")

    def test_empty_input_is_a_valid_empty_matrix(self):
        self.assertEqual(evaluate_responsibilities([]), [])
        self.assertEqual(load_matrix(LocalServiceAdapter(records=())), [])

    def test_adapter_failure_is_reported_with_context(self):
        def failing_adapter():
            raise AdapterError("offline fixture unavailable")

        with self.assertRaisesRegex(ServiceAdapterError, "offline fixture unavailable"):
            load_matrix(failing_adapter)

    def test_malformed_records_are_rejected(self):
        malformed_examples = (
            ("not a list", "adapter result must be a list"),
            ([None], "record 0 must be a dictionary"),
            ([{"service_model": "IaaS", "responsible_party": "customer"}], "non-empty task"),
            ([{"task": "Review", "service_model": "Unknown", "responsible_party": "customer"}],
             "invalid service_model"),
        )

        for records, message in malformed_examples:
            with self.subTest(records=records):
                with self.assertRaisesRegex(MatrixInputError, message):
                    evaluate_responsibilities(records)

    def test_deliberately_wrong_expectation_raises_assertion(self):
        actual = evaluate_responsibilities(
            [{"task": "Patch OS", "service_model": "IaaS", "responsible_party": "customer"}]
        )

        with self.assertRaises(AssertionError):
            self.assertEqual(actual[0]["responsible_party"], "provider")


if __name__ == "__main__":
    unittest.main()
