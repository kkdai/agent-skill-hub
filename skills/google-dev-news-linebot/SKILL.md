---
name: google-dev-news-linebot
description: Use when searching for the latest Google Developers / Gemini / Agent Platform news and generating LINE Bot application ideas based on those news using the Gemini API.
---

# Google Developers News → LINE Bot Idea Generator

## Overview

This skill fetches the latest news from Google Developers Blog, Google AI Blog, Google Cloud Blog, and DeepMind Blog, filters articles related to **Gemini** and **Agent Platform**, then uses the **Gemini API** to generate **5 actionable LINE Bot application ideas** based on the current news.

## When to Use

- User wants to know the latest Google AI / Gemini / Agent Platform news.
- User wants to brainstorm LINE Bot ideas inspired by cutting-edge Google AI features.
- User needs to quickly evaluate what new Gemini capabilities can be applied to a LINE Bot product.
- User is preparing a pitch or proposal for a Gemini-powered LINE Bot.

## Prerequisites

Ensure the following are installed and configured before running:

```bash
pip install feedparser google-generativeai python-dotenv requests
```

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-2.5-pro   # optional, defaults to gemini-2.5-pro
```

## Core Pattern

```bash
# Generate ideas in Traditional Chinese (default)
python skills/google-dev-news-linebot/scripts/fetch_news.py

# Generate ideas in English
python skills/google-dev-news-linebot/scripts/fetch_news.py --lang en

# Output as JSON (useful for piping to other tools)
python skills/google-dev-news-linebot/scripts/fetch_news.py --output json

# Only fetch news without generating ideas
python skills/google-dev-news-linebot/scripts/fetch_news.py --no-ideas
```

## Quick Reference

| Argument | Values | Default | Description |
|----------|--------|---------|-------------|
| `--output` | `markdown`, `json` | `markdown` | Output format |
| `--lang` | `zh`, `en` | `zh` | Language for generated ideas |
| `--no-ideas` | flag | off | Skip Gemini idea generation |

## News Sources

| Source | Feed URL |
|--------|----------|
| Google Developers Blog | `https://developers.googleblog.com/feeds/posts/default` |
| Google AI Blog | `https://blog.google/technology/ai/rss` |
| Google Cloud Blog (AI & ML) | `https://cloud.google.com/blog/products/ai-machine-learning/rss` |
| Google DeepMind Blog | `https://deepmind.google/blog/rss.xml` |

## Keyword Filter

Articles are filtered by these keywords (case-insensitive):
`gemini`, `agent`, `adk`, `agentspace`, `vertex ai`, `google ai studio`, `generative ai`, `multimodal`, `llm`, `agent development kit`, `firebase genkit`, `langchain google`, `gemma`

## Output Format

### Markdown (Default)

```
# Google Developers News → LINE Bot Ideas

## 📰 Latest Relevant News
1. [Google AI Blog] Gemini 2.5 Pro is now available...
   🔗 https://...
   📅 Sat, 19 Jul 2026 ...

## 💡 LINE Bot Application Ideas

### 1. 📸 GemBot 視覺助理
**核心功能**：...
**使用的 Google AI 技術**：Gemini 2.5 Pro multimodal...
...
```

### JSON

```json
{
  "fetched_at": "2026-07-19T13:00:00+00:00",
  "articles": [ { "source": "...", "title": "...", ... } ],
  "linebot_ideas": "..."
}
```

## Implementation Steps

1. **Set up credentials**: Add `GEMINI_API_KEY` to `.env`.
2. **Install dependencies**: `pip install feedparser google-generativeai python-dotenv requests`.
3. **Run the script**: `python skills/google-dev-news-linebot/scripts/fetch_news.py`.
4. **Review output**: The script prints a news summary followed by 5 LINE Bot ideas.
5. **Use with LINE Bot skills**: Combine output with `line-messaging-api` or `line-liff-api` skills to implement the chosen idea.

## Integration with Other Skills

After generating ideas, use these companion skills to implement them:

| Skill | Use Case |
|-------|----------|
| `line-messaging-api` | Webhook setup, reply/push messages, rich menus |
| `line-liff-api` | LIFF app integration for richer UI experiences |
| `gcp-helper` | Deploy the bot to Cloud Run or GKE |

## Common Mistakes

- **No articles found**: Some RSS feeds may block automated requests. The script gracefully skips failed feeds and continues with others.
- **Empty ideas output**: Check that `GEMINI_API_KEY` is set and valid in `.env`.
- **Outdated news**: RSS feeds typically contain the latest 10–20 posts. Run the script regularly (e.g., daily via cron) to stay updated.
- **Rate limits**: If running frequently, consider caching the fetched articles locally to avoid hitting RSS rate limits.
