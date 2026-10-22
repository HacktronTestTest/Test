"""Tiny intentionally-vulnerable Flask app used as a scan fixture.

This is NOT production code. It exists so the enterprise smoke test has a small,
self-contained scan target with obvious findings (command injection, SSRF, a
hardcoded secret) without needing an external repository or network access.
"""

import os
import sqlite3
import subprocess

import requests
from flask import Flask, request

app = Flask(__name__)

# Hardcoded credential (finding: secret in source).
API_TOKEN = "sk-live-DO-NOT-USE-1234567890abcdef"


@app.route("/ping")
def ping():
    # Command injection: user input flows into a shell.
    host = request.args.get("host", "127.0.0.1")
    return subprocess.check_output("ping -c 1 " + host, shell=True)


@app.route("/fetch")
def fetch():
    # SSRF: user-controlled URL fetched server-side with no allowlist.
    url = request.args.get("url", "")
    return requests.get(url, timeout=5).text


@app.route("/users")
def users():
    name = request.args.get("name", "")
    conn = sqlite3.connect("app.db")
    rows = conn.execute("SELECT id, email FROM users WHERE name = '" + name + "'").fetchall()
    return {"users": rows}


@app.route("/redirect")
def go():
    # Open redirect: next is used as-is.
    return app.redirect(request.args.get("next", "/"))


@app.route("/run")
def run():
    # Another command-injection sink.
    cmd = request.args.get("cmd", "id")
    os.system(cmd)
    return "ok"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
