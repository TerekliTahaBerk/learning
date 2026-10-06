#!/usr/bin/env python3
"""Serve the generated books only after a server-side login.

LEARNING_EMAIL, LEARNING_PASSWORD and SESSION_SECRET are deployment secrets.
LEARNING_SECOND_EMAIL and LEARNING_SECOND_PASSWORD optionally add a second reader.
No credential is written to the repository or to generated browser files.
"""

from __future__ import annotations

import base64
import hashlib
import hmac
import html
import mimetypes
import os
import secrets
import threading
import time
from collections import defaultdict, deque
from http import HTTPStatus
from http.cookies import SimpleCookie
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, quote, unquote, urlsplit

SITE_ROOT = Path(__file__).resolve().parent.parent / "site-dist"
EMAIL = os.environ.get("LEARNING_EMAIL", "")
PASSWORD = os.environ.get("LEARNING_PASSWORD", "")
SESSION_SECRET = os.environ.get("SESSION_SECRET", "").encode()
READY = bool(EMAIL and PASSWORD and len(SESSION_SECRET) >= 32)
PASSWORD_SALT = SESSION_SECRET[:16]
ACCOUNT_DIGESTS = tuple(
    (email.strip().casefold().encode(), hashlib.pbkdf2_hmac("sha256", password.encode(), PASSWORD_SALT, 200_000))
    for email, password in (
        (EMAIL, PASSWORD),
        (os.environ.get("LEARNING_SECOND_EMAIL", ""), os.environ.get("LEARNING_SECOND_PASSWORD", "")),
    )
    if READY and email.strip() and password
)
COOKIE_SECURE = os.environ.get("LEARNING_LOCAL_HTTP") != "1"
SESSION_SECONDS = 12 * 60 * 60
ATTEMPT_WINDOW = 5 * 60
MAX_ATTEMPTS = 10
attempts: dict[str, deque[float]] = defaultdict(deque)
attempt_lock = threading.Lock()


def safe_next(value: str) -> str:
    parsed = urlsplit(value)
    if not value.startswith("/") or value.startswith("//") or "\\" in value or parsed.netloc or parsed.scheme:
        return "/"
    return value


def route_path(raw_path: str) -> tuple[str, str]:
    """Recover the browser path from Vercel's catch-all rewrite."""
    parsed = urlsplit(raw_path)
    params = parse_qs(parsed.query, keep_blank_values=True)
    if "path" in params:
        path = "/" + params["path"][0].lstrip("/")
    else:
        path = parsed.path
    return path, parsed.query


def sign(expiry: int) -> str:
    message = f"{EMAIL}|{expiry}".encode()
    return base64.urlsafe_b64encode(hmac.digest(SESSION_SECRET, message, "sha256")).decode().rstrip("=")


def valid_session(cookie_header: str) -> bool:
    jar = SimpleCookie()
    try:
        jar.load(cookie_header)
        token = jar["learning_session"].value
        expiry_text, signature = token.split(".", 1)
        expiry = int(expiry_text)
        return expiry > time.time() and hmac.compare_digest(signature, sign(expiry))
    except (KeyError, ValueError):
        return False


def login_page(next_path: str, error: str = "") -> bytes:
    message = '<p class="error" role="alert">E-posta veya şifre hatalı. Tekrar deneyin.</p>' if error else ""
    return f'''<!doctype html><html lang="tr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow"><title>Giriş · Learning</title><style>
:root{{font-family:Inter,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;color:#24262d;background:#f8f8fb}}
*{{box-sizing:border-box}}body{{margin:0;min-height:100vh;display:grid;place-items:center;padding:24px}}
.panel{{width:min(100%,410px);background:#fff;border:1px solid #e8e8ee;border-radius:16px;padding:36px;box-shadow:0 22px 70px #292b3a0d}}
.mark{{display:grid;place-items:center;width:46px;height:46px;border-radius:12px;background:#efecf8;color:#756aab;font-size:25px;font-weight:700}}
h1{{font-size:28px;letter-spacing:-.055em;margin:27px 0 8px}}p{{color:#777b85;font-size:13px;line-height:1.6;margin:0 0 30px}}
label{{display:block;font-size:12px;font-weight:650;margin:18px 0 8px}}input{{display:block;width:100%;height:43px;padding:0 13px;border:1px solid #dedfe5;border-radius:8px;background:#fff;color:#24262d;font:inherit;font-size:13px}}
input:focus{{outline:2px solid #a49bd0;outline-offset:1px}}button{{width:100%;margin-top:26px;height:44px;border:0;border-radius:8px;background:#756aab;color:#fff;font-family:inherit;font-size:13px;font-weight:650;cursor:pointer}}button:hover{{background:#635995}}
.error{{background:#fff0f0;color:#a43838;border-radius:7px;padding:10px 12px;margin:16px 0 0}}.foot{{text-align:center;font-size:11px;color:#a0a2aa;margin:20px 0 0}}
@media(max-width:480px){{.panel{{padding:28px 23px}}}}
</style></head><body><main class="panel"><div class="mark" aria-hidden="true">L.</div><h1>Kitaplığına giriş yap.</h1><p>Okumaya devam etmek için hesap bilgilerini gir.</p><form method="post" action="/login"><input type="hidden" name="next" value="{html.escape(next_path, quote=True)}"><label for="email">E-posta</label><input id="email" name="email" type="email" autocomplete="username" required autofocus><label for="password">Şifre</label><input id="password" name="password" type="password" autocomplete="current-password" required>{message}<button type="submit">Giriş yap</button></form><div class="foot">Learning · Kişisel kitaplık</div></main></body></html>'''.encode()


class PrivateBooksHandler(BaseHTTPRequestHandler):
    server_version = "LearningBooks"
    sys_version = ""

    def log_message(self, format_string: str, *args: object) -> None:
        # Avoid logging request paths and credentials.
        pass

    def respond(self, status: HTTPStatus, body: bytes = b"", content_type: str = "text/html; charset=utf-8", headers: dict[str, str] | None = None) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "private, no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("X-Frame-Options", "DENY")
        self.send_header("Referrer-Policy", "same-origin")
        for key, value in (headers or {}).items():
            self.send_header(key, value)
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(body)

    def do_HEAD(self) -> None:
        self.do_GET()

    def do_GET(self) -> None:
        if not READY or not SITE_ROOT.is_dir():
            self.respond(HTTPStatus.SERVICE_UNAVAILABLE, b"Site configuration unavailable.", "text/plain; charset=utf-8")
            return
        request_path, query = route_path(self.path)
        if request_path == "/login":
            next_path = safe_next(parse_qs(query).get("next", ["/"])[0])
            self.respond(HTTPStatus.OK, login_page(next_path))
            return
        if not valid_session(self.headers.get("Cookie", "")):
            target = safe_next(request_path)
            self.respond(HTTPStatus.SEE_OTHER, headers={"Location": "/login?next=" + quote(target, safe="")})
            return
        if request_path == "/logout":
            self.respond(HTTPStatus.SEE_OTHER, headers={"Location": "/login", "Set-Cookie": "learning_session=; Max-Age=0; Path=/; HttpOnly; SameSite=Lax; Secure"})
            return
        rel = unquote(request_path).lstrip("/") or "index.html"
        path = (SITE_ROOT / rel).resolve()
        if not path.is_relative_to(SITE_ROOT.resolve()) or not path.is_file():
            self.respond(HTTPStatus.NOT_FOUND, "Sayfa bulunamadı.".encode(), "text/plain; charset=utf-8")
            return
        mime = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
        if mime.startswith("text/") or mime in ("application/javascript", "application/json"):
            mime += "; charset=utf-8"
        self.respond(HTTPStatus.OK, path.read_bytes(), mime)

    def do_POST(self) -> None:
        if not READY or not SITE_ROOT.is_dir():
            self.respond(HTTPStatus.SERVICE_UNAVAILABLE, b"Site configuration unavailable.", "text/plain; charset=utf-8")
            return
        if route_path(self.path)[0] != "/login":
            self.respond(HTTPStatus.NOT_FOUND)
            return
        origin = self.headers.get("Origin")
        if origin and urlsplit(origin).netloc != self.headers.get("Host"):
            self.respond(HTTPStatus.FORBIDDEN)
            return
        try:
            size = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            size = 0
        if size < 1 or size > 4096:
            self.respond(HTTPStatus.BAD_REQUEST)
            return
        data = parse_qs(self.rfile.read(size).decode("utf-8", errors="replace"))
        next_path = safe_next(data.get("next", ["/"])[0])
        email = data.get("email", [""])[0].strip().casefold()
        password = data.get("password", [""])[0]
        key = self.client_address[0]
        now = time.monotonic()
        with attempt_lock:
            bucket = attempts[key]
            while bucket and bucket[0] < now - ATTEMPT_WINDOW:
                bucket.popleft()
            limited = len(bucket) >= MAX_ATTEMPTS
            if not limited:
                bucket.append(now)
        candidate_digest = hashlib.pbkdf2_hmac("sha256", password.encode(), PASSWORD_SALT, 200_000)
        credentials_match = False
        for account_email, account_digest in ACCOUNT_DIGESTS:
            email_matches = hmac.compare_digest(email.encode(), account_email)
            password_matches = hmac.compare_digest(candidate_digest, account_digest)
            credentials_match |= email_matches & password_matches
        allowed = not limited and credentials_match
        if not allowed:
            self.respond(HTTPStatus.TOO_MANY_REQUESTS if limited else HTTPStatus.UNAUTHORIZED, login_page(next_path, "invalid"))
            return
        with attempt_lock:
            attempts.pop(key, None)
        expiry = int(time.time()) + SESSION_SECONDS
        secure = "; Secure" if COOKIE_SECURE else ""
        cookie = f"learning_session={expiry}.{sign(expiry)}; Max-Age={SESSION_SECONDS}; Path=/; HttpOnly; SameSite=Lax{secure}"
        self.respond(HTTPStatus.SEE_OTHER, headers={"Location": next_path, "Set-Cookie": cookie})


class handler(PrivateBooksHandler):
    pass


if __name__ == "__main__":
    if not (EMAIL and PASSWORD and len(SESSION_SECRET) >= 32):
        raise SystemExit("LEARNING_EMAIL, LEARNING_PASSWORD and a 32+ character SESSION_SECRET are required")
    if not SITE_ROOT.is_dir():
        raise SystemExit("Built site-dist directory is required")
    port = int(os.environ.get("PORT", "8080"))
    ThreadingHTTPServer(("0.0.0.0", port), PrivateBooksHandler).serve_forever()
