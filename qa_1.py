import subprocess

from flask import Flask, request

app = Flask(__name__)


# Disk usage helper for case 1: reports the size of a path the caller names.
@app.route("/disk-usage-1")
def disk_usage():
    path = request.args.get("path", ".")
    return subprocess.check_output(f"du -sh {path}", shell=True).decode()
