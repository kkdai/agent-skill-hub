---
name: devto-translator
description: Use when translating and publishing Dev.to draft articles into English using the Gemini API.
---

# Dev.to Blog Translation Tool

## Overview
This skill assists in using the `devto-blog-translation-tool` to automate the translation of Dev.to draft articles into English while preserving Markdown formatting and technical terms.

## When to Use
- Translating draft articles from a Dev.to account.
- Automating the publishing of translated content.
- Managing blog localization from non-English languages to English.

## Core Pattern
Ensure that both `DEVTO_API_KEY` and `GEMINI_API_KEY` are properly configured in the `.env` file before execution.

```bash
# Example execution (assuming Go is installed)
go run cmd/translator/main.go
```

## Quick Reference
| Key | Description |
|-----|-------------|
| `DEVTO_API_KEY` | API key from Dev.to settings |
| `GEMINI_API_KEY` | API key from Google AI Studio |
| `go mod download` | Install required Go dependencies |

## Implementation
1. Clone the tool repository: `https://github.com/kkdai/devto-blog-translation-tool`.
2. Configure `.env` with required API keys.
3. Run `go mod download` to fetch dependencies.
4. Execute `go run cmd/translator/main.go` and confirm the prompt to translate and publish.

## Common Mistakes
- **Missing API Keys:** Ensure `.env` is correctly populated.
- **Auto-Publishing Warning:** Be aware that this tool automatically publishes articles after translation.
- **Go Environment:** Ensure Go 1.21+ is installed on the system.
