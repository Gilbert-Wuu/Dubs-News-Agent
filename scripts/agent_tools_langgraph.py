from typing import TypedDict, List
from langgraph.graph import StateGraph, END
from web_scrape import scrape_articles
from summarization import create_digest
from notify_whatsapp import send_whatsapp
import datetime
from dotenv import load_dotenv

load_dotenv()


class AgentState(TypedDict):
    keyword: str
    scraped_articles: List[dict]
    digest: str
    article_links: List[dict]
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
    print(f"\n[summarize] Creating digest from {len(articles)} articles")
    result = create_digest(articles)
    print(f"[summarize] Digest created")
    return {"digest": result["digest"], "article_links": result["articles"]}


def notify_node(state: AgentState) -> dict:
    digest = state["digest"]
    article_links = state["article_links"]
    print(f"\n[notify] Sending WhatsApp digest with {len(article_links)} source links")
    date_str = datetime.date.today().strftime("%b %d")
    send_whatsapp(f"\U0001f3c0 Warriors Daily — {date_str}\n\n{digest}")
    sources_lines = ["\U0001f4ce Sources:"]
    for a in article_links[:3]:
        sources_lines.append(f"- {a['title']}: {a['url']}")
    send_whatsapp("\n".join(sources_lines))
    return {"notification_sent": True}


# --- Conditional routers ---

def route_after_scrape(state: AgentState) -> str:
    if state.get("scraped_articles"):
        return "summarize"
    print("[router] No articles found — stopping pipeline")
    return END


def route_after_summarize(state: AgentState) -> str:
    if state.get("digest"):
        return "notify"
    print("[router] No digest generated — stopping pipeline")
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
    print(f"Digest created    : {bool(result.get('digest'))}")
    print(f"Notification sent : {result.get('notification_sent', False)}")
