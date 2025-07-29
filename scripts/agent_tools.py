from pydantic import BaseModel, Field
from typing import List
from web_scrape import scrape_articles
from summarization import summarize_articles
from notify_email import send_email
from langchain_core.tools import StructuredTool

# --- Tool 1: Scrape ---

class ScrapeInput(BaseModel):
    keyword: str = Field(description="NBA team or player to search for")

def scrape_tool(keyword: str) -> List[dict]:
    """Scrape NBA news articles containing a keyword."""
    return scrape_articles(keyword=keyword)  # returns list of article dicts

# --- Tool 2: Summarize ---

class SummarizeInput(BaseModel):
    articles: List[dict] = Field(description="List of article dicts (each with keys: 'url', 'title', 'text')")

def summarize_tool(articles: List[dict]) -> List[dict]:
    """Summarize a list of news articles using LLM."""
    return summarize_articles(articles)

# --- Tool 3: Notify ---

class NotifyInput(BaseModel):
    summaries: List[dict] = Field(description="List of summarized articles (dicts with 'title', 'summary', 'url')")
    subject: str = Field(description="Email subject")

def notify_tool(summaries: List[dict], subject: str) -> str:
    """Send an email notification with the summaries."""
    body = "\n\n".join([f"Title: {a['title']}\nSummary: {a['summary']}\nURL: {a['url']}" for a in summaries])
    send_email(subject, body)
    return "Email sent!"

# --- Convert to OpenAI Functions ---

scrape_agent_tool = StructuredTool.from_function(
    func=scrape_tool,
    name="scrape_news",
    description="Scrape NBA news articles for a keyword and returns a list of article dictionaries suitable as input for summarize_articles.",
    args_schema=ScrapeInput
)
summarize_agent_tool = StructuredTool.from_function(
    func=summarize_tool,
    name="summarize_articles",
    description="Takes a list of article dictionaries as input. Summarize scraped news articles. Returns a list of summaries with titles and URLs suitable as input for send_notification.",
    args_schema=SummarizeInput
)
notify_agent_tool = StructuredTool.from_function(
    func=notify_tool,
    name="send_notification",
    description="Send an email notification with the summarized articles. The email will include the titles, summaries, and URLs of the articles.",
    args_schema=NotifyInput
)

# --- List for agent ---

AGENT_TOOLS = [scrape_agent_tool, summarize_agent_tool, notify_agent_tool]
