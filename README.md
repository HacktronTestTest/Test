# vulnerable-app (scan fixture)

Intentionally-vulnerable minimal Flask app used only as a target for the
enterprise stack smoke test (`scripts/smoke-test.sh`). It contains obvious
sinks (command injection, SSRF, a hardcoded secret) so an end-to-end scan
produces findings without needing an external repository.

Do not deploy this. `scripts/smoke-test.sh` turns this directory into a local
bare git repo and serves it over HTTP inside the compose network so the scan
engine has something to clone with zero external egress.
