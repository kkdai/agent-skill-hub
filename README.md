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
    └── devto-translator/ # Dev.to Translator skill
        └── SKILL.md
```
