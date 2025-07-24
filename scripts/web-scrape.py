import pandas as pd
import requests
from bs4 import BeautifulSoup
import json
import os
from newspaper import Article

# Load URLs from Excel
DATA_PATH = "./data/urls.xlsx"
df = pd.read_excel(DATA_PATH)
urls = df["URL"].dropna().tolist()

# Choose keyword for filtering
keyword = "Warriors"
output_articles = []

# Mapping for article URL patterns
ARTICLE_PATTERNS = {
    "espn.com": "/story/",
    "yahoo.com": "/article/",
    "nba.com": "/news/",
    "bleacherreport.com": "/articles/"
}

def match_article_pattern(link, base_url):
    for domain, pattern in ARTICLE_PATTERNS.items():
        if domain in base_url and pattern in link:
            return True
    return False

def find_articles_with_keyword(base_url, keyword):
    articles = []
    try:
        res = requests.get(base_url, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")
        for a in soup.find_all("a", href=True):
            href = a["href"]
            text = a.get_text(strip=True)
            # Ensure full URL
            from urllib.parse import urljoin
            url = urljoin(base_url, href)
            # Only consider real article links
            if match_article_pattern(href, base_url):
                # Check if keyword is in title/text
                if keyword.lower() in text.lower():
                    # Fetch the article text
                    try:
                        art = Article(url)
                        art.download()
                        art.parse()
                        article_text = art.text
                    except Exception as e:
                        print(f"Failed to get article text: {url} ({e})")
                        article_text = ""
                    articles.append({
                        "url": url,
                        "title": text,
                        "text": article_text[:15000]  # Truncate if needed for LLMs
                    })
    except Exception as e:
        print(f"Error processing {base_url}: {e}")
    return articles

if __name__ == "__main__":
    for url in urls:
        print(f"Scanning {url}")
        found_articles = find_articles_with_keyword(url, keyword)
        output_articles.extend(found_articles)
    SCRAPED_PATH = "./data/scraped_articles.json"
    with open(SCRAPED_PATH, "w", encoding="utf-8") as f:
        json.dump(output_articles, f, ensure_ascii=False, indent=2)
    print(f"Saved {len(output_articles)} articles mentioning '{keyword}'")