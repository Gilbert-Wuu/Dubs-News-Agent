# <img width="32" height="32" alt="image" src="https://github.com/user-attachments/assets/17c44201-a314-4eb1-9f7b-6238c70c1a4c" /> Dubs News Agent 


**Dubs News Agent** is an automated news pipeline that scrapes the latest articles about the Golden State Warriors from top sports websites and generates concise, LLM-powered summaries. Perfect for Warriors fans and anyone wanting a daily digest of “Dubs” headlines.

---

## Features

- 🔗 **Multi-site Scraping:** Gathers NBA/Warriors news from ESPN, Yahoo Sports, NBA.com, Bleacher Report, and more.
- 🤖 **AI Summarization:** Uses OpenAI GPT to generate brief, readable news summaries.
- 📁 **Modular Code:** Cleanly separates scraping and summarization scripts for easy development.
- 🕒 **Ready for Automation:** Designed for easy scheduling (e.g. daily cron job).
- 🏆 **Warriors Focused:** Built by a Warriors fan, for Warriors fans.

---


## Usage

### 1. **Clone the Repo**
```bash
git clone https://github.com/YOUR_USERNAME/dubs-news-agent.git
cd dubs-news-agent
```

### 2. **Setup you Environment**
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. **Configure your OPENAI API KEY**
- Create a `.env` file in the root directory:
```bash
OPENAI_API_KEY=sk-xxx-your-openai-key
```

### 4. **Prepare your Sources**
- Add or update news site URLs in `data/urls.xlsx`.

---

## Customization
- 📝 Add More Sources: Edit data/urls.xlsx to scrape more sites or different NBA teams.
- 📬 Notifications: Integrate with email, Slack, or Discord to get summaries delivered.
- 🤝 Agentic Workflow: Future versions will include a smart, multi-step agent pipeline.
