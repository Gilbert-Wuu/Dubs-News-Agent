# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
playwright install chromium
```

Create a `.env` file in the root:
```
OPENAI_API_KEY=sk-...
CALLMEBOT_PHONE=+1XXXXXXXXXX
CALLMEBOT_APIKEY=your_callmebot_api_key
```

**Getting a CallMeBot API key (one-time):**
1. Add `+34 694 26 48 06` on WhatsApp
2. Send it: `I allow callmebot to send me messages`
3. You'll receive your API key via WhatsApp

## Running the Pipeline

Run from the repo root:

```bash
python scripts/run_pipeline.py
```

## GitHub Actions (Automatic Daily Run)

The pipeline runs automatically every day at 8:00 AM PST via `.github/workflows/daily_news.yml`.

Add these secrets in your GitHub repo settings → Secrets and variables → Actions:
- `OPENAI_API_KEY`
- `CALLMEBOT_PHONE`
- `CALLMEBOT_APIKEY`

You can also trigger it manually from the GitHub Actions tab.

## Architecture

The pipeline is a LangGraph `StateGraph` defined in `scripts/agent_tools_langgraph.py` and invoked by `scripts/run_pipeline.py`.

**Data flow:**
1. `scrape_node` — scans RSS feeds + NBA.com (via Playwright) for articles matching keyword `"Warriors"` → `data/scraped_articles.json`
2. `summarize_node` — feeds all articles into a single LLM call to produce a 3-bullet-point morning digest → `data/summarized_articles.json`
3. `notify_node` — sends two WhatsApp messages: (1) digest bullets, (2) top 3 source links

Conditional routing: if scrape returns no articles, pipeline stops before summarizing; if summarize returns no digest, pipeline stops before notifying.

## Key Files

- `scripts/agent_tools_langgraph.py` — LangGraph `StateGraph` with scrape/summarize/notify nodes and conditional routing
- `scripts/run_pipeline.py` — entrypoint; invokes the graph
- `scripts/web_scrape.py` — `scrape_articles()`: RSS via `feedparser`, JS-rendered via Playwright
- `scripts/summarization.py` — `create_digest()`: single LLM call across all articles; produces 3 bullet points deduplicating overlapping stories
- `scripts/notify_whatsapp.py` — `send_whatsapp()`: sends message via CallMeBot WhatsApp API
- `.github/workflows/daily_news.yml` — GitHub Actions cron job (8 AM PST daily)
