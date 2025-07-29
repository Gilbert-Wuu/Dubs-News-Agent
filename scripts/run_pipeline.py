from web_scrape import scrape_articles
from summarization import summarize_articles
from notify_email import send_email
import datetime

print(f"\n--- Pipeline started at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ---\n")


def run():
    articles = scrape_articles()
    summaries = summarize_articles(articles)
    if summaries:
        body = "\n\n".join([f"Title: {a['title']}\nSummary: {a['summary']}\nURL: {a['url']}" for a in summaries])
        send_email("Your Daily Dubs Nation News!", body)
    else:
        print("No new summaries to notify.")

if __name__ == "__main__":
    run()
