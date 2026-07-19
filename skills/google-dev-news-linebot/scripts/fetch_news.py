#!/usr/bin/env python3
"""
Google Developers News Fetcher & LINE Bot Idea Generator

Fetches the latest news about Gemini and Agent Platform from Google Developers Blog,
then uses Gemini API to generate 5 LINE Bot application ideas based on the news.

Usage:
    python fetch_news.py [--output json|markdown] [--lang zh|en]

Requirements:
    pip install feedparser google-generativeai python-dotenv requests
"""

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from typing import Optional

import feedparser
import requests
from dotenv import load_dotenv

try:
    import google.generativeai as genai
except ImportError:
    print("Error: google-generativeai not installed. Run: pip install google-generativeai")
    sys.exit(1)

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-pro")

# Google Developers / AI related RSS / Atom feeds
NEWS_SOURCES = [
    {
        "name": "Google Developers Blog",
        "url": "https://developers.googleblog.com/feeds/posts/default",
    },
    {
        "name": "Google AI Blog",
        "url": "https://blog.google/technology/ai/rss",
    },
    {
        "name": "Google Cloud Blog - AI & ML",
        "url": "https://cloud.google.com/blog/products/ai-machine-learning/rss",
    },
    {
        "name": "Google DeepMind Blog",
        "url": "https://deepmind.google/blog/rss.xml",
    },
]

# Keywords to filter relevant articles
KEYWORDS = [
    "gemini",
    "agent",
    "adk",
    "agentspace",
    "vertex ai",
    "google ai studio",
    "generative ai",
    "multimodal",
    "llm",
    "agent development kit",
    "firebase genkit",
    "langchain google",
    "gemma",
]

MAX_ARTICLES_PER_SOURCE = 10
MAX_ARTICLES_FOR_PROMPT = 8


# ---------------------------------------------------------------------------
# News Fetching
# ---------------------------------------------------------------------------

def fetch_feed(source: dict, timeout: int = 10) -> list[dict]:
    """Fetch and parse a single RSS/Atom feed."""
    articles = []
    try:
        feed = feedparser.parse(source["url"])
        for entry in feed.entries[:MAX_ARTICLES_PER_SOURCE]:
            title = entry.get("title", "")
            summary = entry.get("summary", "") or entry.get("description", "")
            link = entry.get("link", "")
            published = entry.get("published", "") or entry.get("updated", "")

            # Strip HTML tags from summary
            import re
            summary = re.sub(r"<[^>]+>", "", summary).strip()
            summary = summary[:500]  # Truncate to keep prompt manageable

            articles.append({
                "source": source["name"],
                "title": title,
                "summary": summary,
                "link": link,
                "published": published,
            })
    except Exception as e:
        print(f"[WARN] Failed to fetch {source['name']}: {e}", file=sys.stderr)
    return articles


def is_relevant(article: dict) -> bool:
    """Check if article contains any of the target keywords."""
    text = (article["title"] + " " + article["summary"]).lower()
    return any(kw in text for kw in KEYWORDS)


def fetch_all_news() -> list[dict]:
    """Fetch news from all sources and filter by keywords."""
    all_articles = []
    for source in NEWS_SOURCES:
        articles = fetch_feed(source)
        all_articles.extend(articles)

    relevant = [a for a in all_articles if is_relevant(a)]

    # Sort by published date (newest first), fall back to original order
    def parse_date(article):
        try:
            from email.utils import parsedate_to_datetime
            return parsedate_to_datetime(article["published"])
        except Exception:
            return datetime.min.replace(tzinfo=timezone.utc)

    relevant.sort(key=parse_date, reverse=True)
    return relevant


# ---------------------------------------------------------------------------
# LINE Bot Idea Generation via Gemini
# ---------------------------------------------------------------------------

def build_prompt(articles: list[dict], lang: str = "zh") -> str:
    """Build the prompt for Gemini to generate LINE Bot ideas."""
    news_text = ""
    for i, article in enumerate(articles[:MAX_ARTICLES_FOR_PROMPT], 1):
        news_text += f"""
{i}. [{article['source']}] {article['title']}
   Published: {article['published']}
   Summary: {article['summary']}
   Link: {article['link']}
"""

    if lang == "zh":
        return f"""你是一位資深的 LINE Bot 開發顧問，同時也是 Google AI 技術的專家。

以下是最新的 Google Developers / AI 相關新聞：

{news_text}

請根據這些最新技術新聞，提出 **5 個具體可行的 LINE Bot 應用創意**。

每個創意需包含：
1. **Bot 名稱**：一個吸引人的名稱
2. **核心功能**：解決什麼問題、提供什麼服務（2-3 句話）
3. **使用的 Google AI 技術**：具體說明使用哪些 Gemini 或 Agent Platform 的功能
4. **LINE Bot 功能亮點**：如 Rich Menu、Flex Message、LIFF、推播通知等特色設計
5. **目標用戶**：誰會使用這個 Bot
6. **實作難度**：簡單 / 中等 / 進階

請用繁體中文回答，格式清晰易讀。
"""
    else:
        return f"""You are a senior LINE Bot developer and Google AI technology expert.

Here are the latest Google Developers / AI related news:

{news_text}

Based on these latest tech news, propose **5 concrete and feasible LINE Bot application ideas**.

Each idea should include:
1. **Bot Name**: An attractive name
2. **Core Functionality**: What problem it solves / what service it provides (2-3 sentences)
3. **Google AI Technology Used**: Specific Gemini or Agent Platform features utilized
4. **LINE Bot Feature Highlights**: Rich Menu, Flex Message, LIFF, push notifications, etc.
5. **Target Users**: Who would use this Bot
6. **Implementation Difficulty**: Easy / Medium / Advanced

Please respond in English with clear formatting.
"""


def generate_linebot_ideas(articles: list[dict], lang: str = "zh") -> str:
    """Use Gemini API to generate LINE Bot ideas based on news articles."""
    if not GEMINI_API_KEY:
        return "Error: GEMINI_API_KEY not set. Please add it to your .env file."

    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel(GEMINI_MODEL)

    prompt = build_prompt(articles, lang)

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error calling Gemini API: {e}"


# ---------------------------------------------------------------------------
# Output Formatting
# ---------------------------------------------------------------------------

def format_news_summary(articles: list[dict]) -> str:
    """Format fetched articles as a readable summary."""
    if not articles:
        return "⚠️  No relevant articles found."

    lines = [f"📰 Found {len(articles)} relevant articles:\n"]
    for i, a in enumerate(articles, 1):
        lines.append(f"{i}. [{a['source']}] {a['title']}")
        lines.append(f"   🔗 {a['link']}")
        lines.append(f"   📅 {a['published']}\n")
    return "\n".join(lines)


def output_json(articles: list[dict], ideas: str) -> None:
    """Output results in JSON format."""
    result = {
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "articles": articles,
        "linebot_ideas": ideas,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


def output_markdown(articles: list[dict], ideas: str) -> None:
    """Output results in Markdown format."""
    print("# Google Developers News → LINE Bot Ideas\n")
    print(f"_Generated at: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}_\n")
    print("---\n")
    print("## 📰 Latest Relevant News\n")
    print(format_news_summary(articles))
    print("\n---\n")
    print("## 💡 LINE Bot Application Ideas\n")
    print(ideas)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Fetch Google Dev news & generate LINE Bot ideas with Gemini"
    )
    parser.add_argument(
        "--output",
        choices=["json", "markdown"],
        default="markdown",
        help="Output format (default: markdown)",
    )
    parser.add_argument(
        "--lang",
        choices=["zh", "en"],
        default="zh",
        help="Language for generated ideas (default: zh for Traditional Chinese)",
    )
    parser.add_argument(
        "--no-ideas",
        action="store_true",
        help="Only fetch and display news without generating ideas",
    )
    args = parser.parse_args()

    print("🔍 Fetching Google Developers news...", file=sys.stderr)
    articles = fetch_all_news()
    print(f"✅ Found {len(articles)} relevant articles.", file=sys.stderr)

    ideas = ""
    if not args.no_ideas:
        print(f"🤖 Generating LINE Bot ideas with {GEMINI_MODEL}...", file=sys.stderr)
        ideas = generate_linebot_ideas(articles, lang=args.lang)
        print("✅ Ideas generated.", file=sys.stderr)

    if args.output == "json":
        output_json(articles, ideas)
    else:
        output_markdown(articles, ideas)


if __name__ == "__main__":
    main()
