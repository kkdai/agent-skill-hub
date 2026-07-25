# Agent Skill Hub

A collection of specialized skills for AI agents.

## How to Install

You can install this skill hub in your Claude Code environment using:

```bash
claude plugin add https://github.com/al03034132/agent-skill-hub
```

Or for local development:

```bash
claude plugin add ./path/to/agent-skill-hub
```

## Available Skills

- **gcp-helper**: Helper for GCP resource management.
- **n8n-executor**: Executor for n8n workflows.
- **devto-translator**: Automate Dev.to draft translations into English.
- **line-messaging-api**: Build, debug, and manage LINE Bots via LINE Messaging API.
- **line-liff-api**: Build, debug, and manage LINE front-end apps (LIFF) via LIFF JS SDK.
- **line-login**: Integrate, build, and debug LINE Login v2.1 (OAuth 2.0 / OpenID Connect).

## Directory Structure

```text
.
├── plugin.json           # Plugin descriptor
├── README.md             # This file
└── skills/               # Skills directory
    ├── gcp-helper/       # GCP Helper skill
    │   └── SKILL.md      # Core definition
    ├── n8n-executor/     # n8n Executor skill
    │   └── SKILL.md
    ├── devto-translator/ # Dev.to Translator skill
    │   └── SKILL.md
    ├── line-messaging-api/ # LINE Messaging API skill
    │   └── SKILL.md
    ├── line-liff-api/    # LINE LIFF API skill
    │   └── SKILL.md
    └── line-login/       # LINE Login v2.1 skill
        └── SKILL.md
```
