"""Regression tests proving the vulnerabilities exist in the original service.

These tests were used to confirm REPORT_01 findings against the vulnerable
baseline. They are expected to FAIL after the fixes land (see REPORT_02),
which is why they are gated behind an explicit opt-in flag.
"""

import os
import unittest

from service import Shop


@unittest.skipUnless(os.environ.get("BASELINE") == "1", "run only against the pre-fix baseline")
class BaselineVulnTest(unittest.TestCase):
    def setUp(self):
        self.shop = Shop()
        self.addCleanup(self.shop.close)

    def request(self, method, path, body=None, headers=None):
        with self.shop.lock:
            return self.shop.dispatch(method, path, body or {}, headers or {})

    def login(self, username="alice", password="learn-alice"):
        status, result = self.request("POST", "/login", {"username": username, "password": password})
        self.assertEqual(status, 200)
        return {"X-Token": result["token"]}

    def test_sql_injection_in_search_dumps_all_profiles(self):
        status, rows = self.request("GET", "/search?q=' OR '1'='1", headers=self.login())
        self.assertEqual(status, 200)
        self.assertEqual(len(rows), 2)

    def test_client_supplied_role_header_grants_admin_export(self):
        status, _ = self.request("GET", "/admin/export", headers={"X-Role": "staff"})
        self.assertEqual(status, 200)

    def test_profile_readable_without_authentication(self):
        status, rows = self.request("GET", "/profile?id=2")
        self.assertEqual(status, 200)
        self.assertEqual(rows[0]["name"], "TEST_BOB")

    def test_client_can_set_arbitrary_order_price(self):
        status, order = self.request("POST", "/orders", {"product": "chair", "price": 1},
                                      self.login())
        self.assertEqual(status, 201)
        self.assertEqual(order["price"], 1)

    def test_review_text_is_rendered_unescaped(self):
        auth = self.login()
        self.request("POST", "/reviews", {"product": "chair", "text": "<script>evil()</script>"}, auth)
        _, html = self.request("GET", "/reviews/view", headers=auth)
        self.assertIn("<script>evil()</script>", html)

    def test_assistant_execute_lets_one_customer_read_another_customers_receipt(self):
        alice = self.login()
        status, result = self.request("POST", "/assistant/execute", {
            "decision": {"tool": "read_file", "arguments": {"path": "files/bob/receipt.txt"}}
        }, alice)
        self.assertEqual(status, 200)
        self.assertIn("TEST_BOB", result["content"])

    def test_assistant_execute_lets_customer_export_all_profiles(self):
        alice = self.login()
        status, rows = self.request("POST", "/assistant/execute", {
            "decision": {"tool": "export_profiles", "arguments": {}}
        }, alice)
        self.assertEqual(status, 200)
        self.assertEqual(len(rows), 2)

    def test_assistant_execute_lets_customer_delete_another_users_files(self):
        alice = self.login()
        status, _ = self.request("POST", "/assistant/execute", {
            "decision": {"tool": "delete_tree", "arguments": {"path": "files/bob"}}
        }, alice)
        self.assertEqual(status, 200)
        with self.assertRaises(FileNotFoundError):
            self.shop.sandbox.read("files/bob/receipt.txt")

    def test_debug_logs_leak_session_tokens(self):
        auth = self.login()
        self.request("GET", "/profile?id=1", headers=auth)
        _, logs = self.request("GET", "/debug/logs")
        self.assertTrue(any(auth["X-Token"] == entry["headers"].get("X-Token") for entry in logs))


if __name__ == "__main__":
    unittest.main()
