import os
import json
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

SCRAPED_PATH = "./data/scraped_articles.json"
SUMMARY_PATH = "./data/summarized_articles.json"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

MAX_CHARS_PER_ARTICLE = 2000


def create_digest(articles):
    llm = ChatOpenAI(openai_api_key=OPENAI_API_KEY)
    print(f"Using OpenAI model: {llm.model_name}")

    article_blocks = []
    for i, a in enumerate(articles, 1):
        text = a["text"][:MAX_CHARS_PER_ARTICLE]
        article_blocks.append(f"--- Article {i}: {a['title']} ---\n{text}")
    combined = "\n\n".join(article_blocks)

    prompt = (
        f"You are a Warriors news assistant. Below are {len(articles)} articles collected today about the Golden State Warriors.\n\n"
        "Write a morning digest with exactly 3 bullet points (•) covering the most important events. "
        "Deduplicate overlapping stories — if multiple articles cover the same event, mention it only once. "
        "Each bullet should be one concise sentence in English.\n\n"
        f"{combined}\n\n"
        "Respond ONLY with the bullet points. No intro, no conclusion."
    )

    response = llm.invoke(prompt)
    digest = response.content.strip()

    article_links = [{"title": a["title"], "url": a["url"]} for a in articles]

    result = {"digest": digest, "articles": article_links}
    with open(SUMMARY_PATH, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(f"Digest created from {len(articles)} articles. Saved to {SUMMARY_PATH}")

    return result


if __name__ == "__main__":
    with open(SCRAPED_PATH, "r", encoding="utf-8") as f:
        articles = json.load(f)
    create_digest(articles)
