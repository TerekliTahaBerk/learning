"""Authentication regression checks using disposable test-only credentials."""
import importlib.util
import io
import os
import unittest
from pathlib import Path
from unittest.mock import patch
from urllib.parse import urlencode

ROOT = Path(__file__).resolve().parents[1]
PRIMARY = ("first@example.invalid", "test-only-first-password")
SECOND = ("second@example.invalid", "test-only-second-password")


def load_reader(second_email=SECOND[0], second_password=SECOND[1]):
    env = {
        "LEARNING_EMAIL": PRIMARY[0],
        "LEARNING_PASSWORD": PRIMARY[1],
        "LEARNING_SECOND_EMAIL": second_email,
        "LEARNING_SECOND_PASSWORD": second_password,
        "SESSION_SECRET": "disposable-test-session-secret-at-least-32-characters",
    }
    spec = importlib.util.spec_from_file_location("reader_under_test", ROOT / "api/index.py")
    module = importlib.util.module_from_spec(spec)
    with patch.dict(os.environ, env, clear=True):
        spec.loader.exec_module(module)
    return module


def request(module, email, password, path="/login", cookie="", origin=None):
    body = urlencode({"email": email, "password": password, "next": "/yds/README.html"}).encode()

    class Probe(module.PrivateBooksHandler):
        def __init__(self):
            self.path = path
            self.command = "POST"
            self.client_address = ("127.0.0.1", 12345)
            self.headers = {"Content-Length": str(len(body)), "Host": "reader.test", "Cookie": cookie}
            if origin:
                self.headers["Origin"] = origin
            self.rfile = io.BytesIO(body)

        def respond(self, status, body=b"", content_type="text/html; charset=utf-8", headers=None):
            self.result = (status, body, headers or {})

    handler = Probe()
    handler.do_POST()
    return handler


class ReaderAuthTests(unittest.TestCase):
    def setUp(self):
        self.reader = load_reader()

    def test_both_accounts_get_a_valid_secure_session_and_yds_access(self):
        for credentials in (PRIMARY, SECOND):
            with self.subTest(account=credentials[0]):
                handler = request(self.reader, *credentials)
                self.assertEqual(handler.result[0], 303)
                self.assertEqual(handler.result[2]["Location"], "/yds/README.html")
                cookie = handler.result[2]["Set-Cookie"]
                self.assertIn("HttpOnly", cookie)
                self.assertIn("SameSite=Lax", cookie)
                self.assertIn("Secure", cookie)
                self.assertTrue(self.reader.valid_session(cookie))
                handler.headers["Cookie"] = cookie
                handler.path = "/yds/README.html"
                handler.command = "GET"
                handler.do_GET()
                self.assertEqual(handler.result[0], 200)
                self.assertIn(b"YDS", handler.result[1])

    def test_passwords_cannot_be_mixed_between_accounts(self):
        for email, password in ((PRIMARY[0], SECOND[1]), (SECOND[0], PRIMARY[1]),
                                (SECOND[0], "incorrect"), ("unknown@example.invalid", SECOND[1])):
            with self.subTest(email=email):
                handler = request(self.reader, email, password)
                self.assertEqual(handler.result[0], 401)
                self.assertNotIn("Set-Cookie", handler.result[2])

    def test_email_normalisation_and_non_ascii_unknown_input(self):
        self.assertEqual(request(self.reader, "  SECOND@EXAMPLE.INVALID  ", SECOND[1]).result[0], 303)
        self.assertEqual(request(self.reader, "özgür@example.invalid", SECOND[1]).result[0], 401)

    def test_missing_or_partial_secondary_configuration_keeps_primary_only(self):
        for email, password in (("", ""), (SECOND[0], ""), ("", SECOND[1])):
            with self.subTest(email_configured=bool(email), password_configured=bool(password)):
                reader = load_reader(email, password)
                self.assertEqual(len(reader.ACCOUNT_DIGESTS), 1)
                self.assertEqual(request(reader, *PRIMARY).result[0], 303)
                self.assertEqual(request(reader, *SECOND).result[0], 401)

    def test_rate_limit_still_blocks_valid_secondary_credentials(self):
        for _ in range(self.reader.MAX_ATTEMPTS):
            self.assertEqual(request(self.reader, SECOND[0], "incorrect").result[0], 401)
        self.assertEqual(request(self.reader, *SECOND).result[0], 429)

    def test_origin_check_still_rejects_cross_site_login(self):
        handler = request(self.reader, *SECOND, origin="https://other.test")
        self.assertEqual(handler.result[0], 403)
        self.assertNotIn("Set-Cookie", handler.result[2])


if __name__ == "__main__":
    unittest.main()
