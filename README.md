# <img width="32" height="32" alt="image" src="https://github.com/user-attachments/assets/17c44201-a314-4eb1-9f7b-6238c70c1a4c" /> Dubs News Agent 


**Dubs News Agent** is an automated pipeline that scrapes, summarizes, and delivers the latest Golden State Warriors news straight to your inbox. Built for Warriors fans and techies who love practical AI and workflow automation.

---

## Features

- 🔗 **Multi-site Scraping:** Gathers news from top NBA news sources (ESPN, Yahoo, NBA.com, Bleacher Report, etc.)
- 🤖 **AI Summarization:** Uses OpenAI GPT to generate brief, readable news summaries.
- 📧 **Email notification** Keep yourself updated with dubs nations daily digest
- 📁 **Modular Code:** Function-based Python scripts for easy extension and reuse.
- 🕒 **Ready for Automation:** Fully automated with cron job scheduling.

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

### 3. **Configure your Secrets**
- Create a `.env` file in the root directory:
```bash
OPENAI_API_KEY=sk-xxx-your-openai-key
EMAIL_ADDRESS=yourgmail@gmail.com
EMAIL_PASSWORD=your_gmail_app_password
TO_EMAIL=destination@email.com
```

### 4. **Prepare your Sources**
- Add or update news site URLs in `data/urls.xlsx`.

### 5. **Run the workflow manually**
```bash
python scripts/run_pipeline.py
```

---

## Automation: Scheduling with Cron
To automate your news digest every day at 10:00 PM:
1. Open your crontab:
```bash
crontab -e
```

2. Add the following line
```bash
0 22 * * * cd /full/path/to/dubs-news-agent && /full/path/to/dubs-news-agent/.venv/bin/python scripts/run_pipeline.py >> pipeline.log 2>&1
```

- All output (including errors) will be logged to `pipeline.log` in your project directory.

---

## Customization
- 📝 Add/modify news sources in `data/urls.xlsx`.
- 📬 Change summary prompt in `scripts/summarization.py` for different tone/length
- 🤝 Agentic Workflow: Future versions will include a smart, multi-step agent pipeline.
