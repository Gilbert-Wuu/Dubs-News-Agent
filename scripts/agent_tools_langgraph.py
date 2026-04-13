from typing import TypedDict, List
from langgraph.graph import StateGraph, END
from web_scrape import scrape_articles
from summarization import summarize_articles
from notify_whatsapp import send_whatsapp
import datetime
from dotenv import load_dotenv

load_dotenv()


class AgentState(TypedDict):
    keyword: str
    scraped_articles: List[dict]
    summaries: List[dict]
    notification_sent: bool


# --- Nodes ---

def scrape_node(state: AgentState) -> dict:
    keyword = state.get("keyword", "Warriors")
    print(f"\n[scrape] Searching for: '{keyword}'")
    articles = scrape_articles(keyword=keyword)

    # Fallback: retry with shorter keyword if nothing found
    if not articles and keyword.lower() != "warriors":
        print(f"[scrape] No results — retrying with 'Warriors'")
        articles = scrape_articles(keyword="Warriors")

    print(f"[scrape] {len(articles)} articles found")
    return {"scraped_articles": articles}


def summarize_node(state: AgentState) -> dict:
    articles = state["scraped_articles"]
    print(f"\n[summarize] Summarizing {len(articles)} articles")
    summaries = summarize_articles(articles)
    print(f"[summarize] {len(summaries)} summaries generated")
    return {"summaries": summaries}


def notify_node(state: AgentState) -> dict:
    summaries = state["summaries"]
    print(f"\n[notify] Sending WhatsApp message with {len(summaries)} summaries")
    date_str = datetime.date.today().strftime("%b %d, %Y")
    lines = [f"Warriors News — {date_str}\n"]
    for i, a in enumerate(summaries, 1):
        lines.append(f"{i}. {a['title']}\n{a['summary']}\n{a['url']}")
    message = "\n\n".join(lines)
    send_whatsapp(message)
    return {"notification_sent": True}


# --- Conditional routers ---

def route_after_scrape(state: AgentState) -> str:
    if state.get("scraped_articles"):
        return "summarize"
    print("[router] No articles found — stopping pipeline")
    return END


def route_after_summarize(state: AgentState) -> str:
    if state.get("summaries"):
        return "notify"
    print("[router] No summaries generated — stopping pipeline")
    return END


# --- Build graph ---

workflow = StateGraph(AgentState)
workflow.add_node("scrape", scrape_node)
workflow.add_node("summarize", summarize_node)
workflow.add_node("notify", notify_node)

workflow.set_entry_point("scrape")
workflow.add_conditional_edges("scrape", route_after_scrape,
                               {"summarize": "summarize", END: END})
workflow.add_conditional_edges("summarize", route_after_summarize,
                               {"notify": "notify", END: END})
workflow.add_edge("notify", END)

graph = workflow.compile()


if __name__ == "__main__":
    result = graph.invoke({"keyword": "Golden State Warriors"})
    print("\n--- Pipeline Complete ---")
    print(f"Articles scraped  : {len(result.get('scraped_articles', []))}")
    print(f"Summaries created : {len(result.get('summaries', []))}")
    print(f"Email sent        : {result.get('notification_sent', False)}")
