# <img width="32" height="32" alt="image" src="https://github.com/user-attachments/assets/17c44201-a314-4eb1-9f7b-6238c70c1a4c" /> Dubs News Agent

**Dubs News Agent** is an automated pipeline that scrapes, summarizes, and delivers the latest Golden State Warriors news to your WhatsApp every morning. Built with LangGraph, LangChain, and GitHub Actions.

---

## Features

- 🔗 **Multi-source Scraping:** Gathers news from 11 RSS feeds (ESPN, Yahoo Sports, CBS Sports, HoopsHype, Bleacher Report, etc.) + NBA.com via Playwright
- 🤖 **AI Summarization:** Uses OpenAI GPT to generate concise, readable summaries focused on the Warriors
- 📱 **WhatsApp Notification:** Delivers your daily digest directly to WhatsApp via CallMeBot
- 🔀 **LangGraph Pipeline:** Stateful `StateGraph` with conditional routing — stops gracefully if no articles or summaries are found
- ⏰ **Fully Automated:** Runs every day at 8 AM EDT via GitHub Actions — no server or local machine required

---

## Setup

### 1. Clone the Repo
```bash
git clone https://github.com/YOUR_USERNAME/dubs-news-agent.git
cd dubs-news-agent
```

### 2. Create a Virtual Environment
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
playwright install chromium
```

### 3. Get a CallMeBot API Key (one-time)
1. Add `+34 694 26 48 06` on WhatsApp
2. Send it: `I allow callmebot to send me messages`
3. You'll receive your personal API key via WhatsApp

### 4. Configure Environment Variables
Create a `.env` file in the repo root:
```
OPENAI_API_KEY=sk-...
CALLMEBOT_PHONE=+1XXXXXXXXXX
CALLMEBOT_APIKEY=your_callmebot_api_key
```

### 5. Run Manually
```bash
python scripts/run_pipeline.py
```

---

## Automation: GitHub Actions

The pipeline runs automatically every day at **8:00 AM EDT** via `.github/workflows/daily_news.yml`.

**Setup:**
1. Go to your repo → **Settings** → **Secrets and variables** → **Actions**
2. Add three repository secrets:

| Secret | Value |
|---|---|
| `OPENAI_API_KEY` | Your OpenAI API key |
| `CALLMEBOT_PHONE` | Your WhatsApp number with country code (e.g. `+12223334444`) |
| `CALLMEBOT_APIKEY` | Your CallMeBot API key |

3. Push your code — the workflow will trigger automatically on schedule, or you can run it manually from the **Actions** tab.

---

## Architecture

The pipeline is a LangGraph `StateGraph` with three nodes and conditional routing:

```
scrape_node → summarize_node → notify_node
     ↓ (no articles)    ↓ (no summaries)
    END                END
```

**Data flow:**
1. `scrape_node` — scans RSS feeds + NBA.com (Playwright) for articles matching `"Warriors"` → `data/scraped_articles.json`
2. `summarize_node` — runs each article through an LLM prompt chain → `data/summarized_articles.json`
3. `notify_node` — formats and sends a WhatsApp message via CallMeBot

---

## Customization

- 📡 **Add RSS sources:** Edit `RSS_SOURCES` in `scripts/web_scrape.py`
- 📝 **Change summary style:** Edit the `PromptTemplate` in `scripts/summarization.py`
- ⏰ **Change schedule:** Edit the cron expression in `.github/workflows/daily_news.yml`
- 🔑 **Change keyword:** Edit `"Golden State Warriors"` in `scripts/run_pipeline.py`
