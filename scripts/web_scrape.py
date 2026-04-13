import feedparser
from bs4 import BeautifulSoup
import json
from newspaper import Article
from urllib.parse import urljoin

SCRAPED_PATH = "./data/scraped_articles.json"
KEYWORD = "Warriors"

# RSS feeds — no JS needed, reliable, free
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

# JS-rendered sources — requires Playwright
PLAYWRIGHT_SOURCES = [
    "https://www.nba.com/warriors/news",
]


def fetch_article_text(url: str) -> tuple:
    """Returns (title, text) for a given article URL using newspaper3k."""
    try:
        art = Article(url)
        art.download()
        art.parse()
        return art.title, art.text[:20000]
    except Exception as e:
        print(f"  Could not fetch article text: {url} ({e})")
        return "", ""


def scrape_rss_sources(keyword: str) -> list:
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

    return articles


def scrape_playwright_sources(keyword: str) -> list:
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("Playwright not installed — skipping JS-rendered sources.")
        return []

    articles = []
    seen_urls = set()
    kw = keyword.lower()

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            for source_url in PLAYWRIGHT_SOURCES:
                print(f"Scanning (Playwright): {source_url}")
                try:
                    page.goto(source_url, timeout=30000)
                    page.wait_for_load_state("networkidle", timeout=15000)
                    html = page.content()
                    soup = BeautifulSoup(html, "html.parser")

                    for a in soup.find_all("a", href=True):
                        href = a["href"]
                        text = a.get_text(strip=True)
                        url  = urljoin(source_url, href)

                        if url in seen_urls or len(text) < 10:
                            continue
                        if kw not in text.lower():
                            continue

                        seen_urls.add(url)
                        fetched_title, article_text = fetch_article_text(url)
                        if article_text:
                            articles.append({
                                "url": url,
                                "title": fetched_title or text,
                                "text": article_text,
                            })
                            print(f"  Found: {text[:80]}")
                except Exception as e:
                    print(f"  Error scanning {source_url}: {e}")

            browser.close()
    except Exception as e:
        print(f"Playwright browser launch failed — skipping JS-rendered sources. ({e})")

    return articles


def scrape_articles(keyword: str = KEYWORD) -> list:
    print(f"\nScraping articles for keyword: '{keyword}'")

    all_articles = []
    seen_urls = set()

    for art in scrape_rss_sources(keyword) + scrape_playwright_sources(keyword):
        if art["url"] not in seen_urls:
            all_articles.append(art)
            seen_urls.add(art["url"])

    with open(SCRAPED_PATH, "w", encoding="utf-8") as f:
        json.dump(all_articles, f, ensure_ascii=False, indent=2)

    print(f"\nTotal: {len(all_articles)} articles saved to {SCRAPED_PATH}")
    return all_articles


if __name__ == "__main__":
    scrape_articles()
