#!/usr/bin/env python3
"""Pull project variables from the Data Jar iOS bridge and store them in .env.

Config (environment or .env.bridge-less): DATAJAR_BRIDGE_URL, DATAJAR_BRIDGE_TOKEN, DATAJAR_KEYS.
Alternatively pipe the bridge JSON on stdin with --stdin.
The output file is written with mode 0600 and is git-ignored.
"""
import argparse, json, os, re, sys, urllib.request

KEY_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


def fetch(url, token, keys):
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"} if token else {})
    if keys:
        req.add_header("X-Requested-Keys", ",".join(keys))
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.load(r)


def quote(v):
    return '"' + str(v).replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n") + '"'


def write_env(path, values):
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w") as f:
        for k, v in sorted(values.items()):
            f.write(f"{k}={quote(v)}\n")
    os.chmod(path, 0o600)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--out", default=".env")
    p.add_argument("--stdin", action="store_true", help="read JSON from stdin instead of the bridge")
    a = p.parse_args()
    keys = [k.strip() for k in os.environ.get("DATAJAR_KEYS", "").split(",") if k.strip()]
    if a.stdin:
        data = json.load(sys.stdin)
    else:
        url = os.environ.get("DATAJAR_BRIDGE_URL")
        if not url:
            sys.exit("DATAJAR_BRIDGE_URL is not set")
        data = fetch(url, os.environ.get("DATAJAR_BRIDGE_TOKEN"), keys)
    if not isinstance(data, dict):
        sys.exit("Bridge must return a JSON object")
    values = {k: v for k, v in data.items() if KEY_RE.match(k) and (not keys or k in keys)}
    missing = [k for k in keys if k not in values]
    if missing:
        sys.exit("Missing keys from bridge: " + ", ".join(missing))
    write_env(a.out, values)
    print(f"Stored {len(values)} variable(s) in {a.out} (mode 600)")


if __name__ == "__main__":
    main()
