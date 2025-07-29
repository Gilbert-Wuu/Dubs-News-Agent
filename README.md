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

---

## Project Progress & Current Status

### Method Tried
**1. LangChain Agent (OPENAI_FUNCTIONS)**
   - **Approach**: \
     Used `AgentType.OPENAI_FUNCTIONS` agent to enable tool-calling with OpenAI models.
   - **Result**: \
     The agent could correctly identify and call each tool (scrape, summarize, notify).
   - **Bottleneck:** \
     _**Could not chain outputs**_ — the agent failed to pass the output of one tool (e.g., scraped articles) as input to the next (summarization), instead invoking downstream tools with empty dictionary.

**2. LangChain ReAct Agent (ZERO_SHOT_REACT_DESCRIPTION / create_react_agent)**
   - **Approach**: \
     Tried both the prebuilt `AgentType.ZERO_SHOT_REACT_DESCRIPTION` and custom `create_react_agent` with ReAct-style prompting for more flexible tool routing and better reasoning.
   - **Result**: \
     Could reason through tool usage, but does not support multi-field/multi-input tools (e.g., cannot handle tools that require a dict or complex input schema).
   - **Limitation:** \
     ZeroShot/ReAct agents expect simple (single string) inputs and cannot process the structured data needed to chain tool outputs.

### Current Bottleneck
- Neither `OPENAI_FUNCTIONS` nor `ReAct agents` fully support passing structured (multi-field) outputs from one tool to another.
- As a result, complex workflows (such as chaining scraping → summarization → notification, with rich data between steps) are not achievable with these agent types.
  
---

## Next Steps: Moving to LangGraph
- **Why LangGraph?** \
  LangGraph’s `StateGraph` enables explicit control over state passing between workflow nodes.
- **Future plan:** \
  Refactor the agent pipeline using LangGraph, where each node represents a tool and receives the full state—including outputs from previous steps. This should allow seamless chaining of outputs and more sophisticated workflows.

