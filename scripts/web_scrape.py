import feedparser
import json
from newspaper import Article

SCRAPED_PATH = "./data/scraped_articles.json"
KEYWORD = "Warriors"

RSS_SOURCES = {
    "ESPN NBA":              "https://www.espn.com/espn/rss/nba/news",
    "Yahoo Sports NBA":      "https://sports.yahoo.com/nba/rss.xml",
    "CBS Sports NBA":        "https://www.cbssports.com/rss/headlines/nba/",
    "HoopsHype":             "https://hoopshype.com/feed/",
    "Golden State of Mind":  "https://www.goldenstateofmind.com/rss/current",
    "ClutchPoints Warriors": "https://clutchpoints.com/golden-state-warriors/feed",
    "Bleacher Report NBA":   "https://bleacherreport.com/articles/feed?tag_id=5",
    "Sporting News NBA":     "https://www.sportingnews.com/us/nba/rss.xml",
    "USA Today NBA":         "https://www.usatoday.com/sports/nba/rss/",
    "NBC Sports NBA":        "https://nbcsports.com/nba/rss",
    "SB Nation NBA":         "https://www.sbnation.com/nba/rss/current",
}


def fetch_article_text(url: str) -> tuple:
    try:
        art = Article(url)
        art.download()
        art.parse()
        return art.title, art.text[:20000]
    except Exception as e:
        print(f"  Could not fetch article text: {url} ({e})")
        return "", ""


def scrape_articles(keyword: str = KEYWORD) -> list:
    print(f"\nScraping articles for keyword: '{keyword}'")

    articles = []
    seen_urls = set()
    kw = keyword.lower()

    for name, feed_url in RSS_SOURCES.items():
        print(f"Scanning RSS: {name}")
        try:
            feed = feedparser.parse(feed_url)
            for entry in feed.entries:
                title   = entry.get("title", "")
                summary = entry.get("summary", "")
                url     = entry.get("link", "")

                if not url or url in seen_urls:
                    continue
                if kw not in title.lower() and kw not in summary.lower():
                    continue

                seen_urls.add(url)
                _, text = fetch_article_text(url)
                articles.append({"url": url, "title": title, "text": text})
                print(f"  Found: {title[:80]}")
        except Exception as e:
            print(f"  Error scanning {name}: {e}")

    with open(SCRAPED_PATH, "w", encoding="utf-8") as f:
        json.dump(articles, f, ensure_ascii=False, indent=2)

    print(f"\nTotal: {len(articles)} articles saved to {SCRAPED_PATH}")
    return articles


if __name__ == "__main__":
    scrape_articles()
