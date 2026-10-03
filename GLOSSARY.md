# Project Glossary

- **Data Jar**: An iOS app that stores key/value data (text, numbers, dictionaries) and exposes it to Shortcuts and automations.
- **iOS bridge**: A Shortcut (or small web endpoint triggered by one) that reads values from Data Jar on the iPhone/iPad and returns them as JSON to other machines/tools.
- **Project variables**: Named values (e.g. API keys, tokens, config) the project needs at runtime. Held in Data Jar, pulled via the bridge, and written to a local, git-ignored `.env`.
- **Secret**: A project variable that must never be committed (API keys, tokens).
