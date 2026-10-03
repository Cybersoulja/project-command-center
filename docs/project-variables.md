# Project Variables via Data Jar

1. In Data Jar, store each secret under its variable name (e.g. `OPENAI_API_KEY`).
2. Create an iOS Shortcut that reads those values and returns a JSON object, exposed to your machine (e.g. via a local HTTP endpoint protected by a bearer token).
3. Copy `.env.example` to your shell env, set `DATAJAR_BRIDGE_URL`, `DATAJAR_BRIDGE_TOKEN`, `DATAJAR_KEYS`.
4. Run `python3 scripts/sync_secrets.py` (or `echo '{"A":"b"}' | python3 scripts/sync_secrets.py --stdin`).

Secrets are written to `.env` (mode 600, git-ignored). Never commit it.
