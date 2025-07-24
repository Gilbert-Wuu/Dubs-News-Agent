import os
import json
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain_community.chat_models import ChatOpenAI


# Load environment variables
load_dotenv()

SCRAPED_PATH = "./data/scraped_articles.json"
SUMMARY_PATH = "./data/summarized_articles.json"

def summarize_articles(articles):
    openai_api_key = os.getenv("OPENAI_API_KEY")
    llm = ChatOpenAI(openai_api_key=openai_api_key)
    print(f"Using OpenAI model: {llm.model_name}")

    prompt = PromptTemplate.from_template(
        "Summarize this NBA news article in 3-5 sentences, focusing on the Golden State Warriors:\n\n{text}\n\nSummary:"
    )
    chain = prompt | llm

    summaries = []
    for article in articles:
        try:
            summary = chain.invoke({"text": article["text"]}) # return AIMessage
            summaries.append({
                "url": article["url"],
                "title": article["title"],
                "summary": summary.content.strip()
            })
        except Exception as e:
            print(f"Failed to summarize {article['url']}: {e}")
    return summaries

if __name__ == "__main__":
    with open(SCRAPED_PATH, "r", encoding="utf-8") as f:
        articles = json.load(f)
    summaries = summarize_articles(articles)
    with open(SUMMARY_PATH, "w", encoding="utf-8") as f:
        json.dump(summaries, f, ensure_ascii=False, indent=2)
    print(f"Summarized {len(summaries)} articles. Results saved to {SUMMARY_PATH}")
