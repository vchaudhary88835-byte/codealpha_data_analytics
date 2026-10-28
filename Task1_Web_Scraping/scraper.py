"""CodeAlpha Task 1: Web Scraping — Books to Scrape practice site."""
from pathlib import Path
import time
import requests
import pandas as pd
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE_URL = "https://books.toscrape.com/"
MAX_PAGES = 3
HEADERS = {"User-Agent": "EducationalDataAnalyticsProject/1.0 (learning exercise)"}

def parse_rating(article):
    paragraph = article.select_one("p.star-rating")
    if not paragraph:
        return "Unknown"
    rating_names = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
    for class_name in paragraph.get("class", []):
        if class_name in rating_names:
            return rating_names[class_name]
    return "Unknown"

def scrape_page(session, page_url):
    response = session.get(page_url, headers=HEADERS, timeout=20)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    books = []
    for article in soup.select("article.product_pod"):
        title_node = article.select_one("h3 a")
        price_node = article.select_one(".price_color")
        availability_node = article.select_one(".availability")
        if not title_node:
            continue
        product_url = urljoin(page_url, title_node.get("href", ""))
        price_text = price_node.get_text(strip=True).replace("£", "").strip() if price_node else ""
        try:
            price_gbp = float(price_text)
        except ValueError:
            price_gbp = None
        books.append({
            "title": title_node.get("title", title_node.get_text(strip=True)),
            "price_gbp": price_gbp,
            "availability": " ".join(availability_node.get_text(" ", strip=True).split()) if availability_node else "Unknown",
            "rating": parse_rating(article),
            "product_url": product_url,
            "source_page": page_url,
        })
    return books, soup

def main():
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    all_books = []
    current_url = BASE_URL
    with requests.Session() as session:
        for page_number in range(1, MAX_PAGES + 1):
            print(f"Scraping page {page_number}: {current_url}")
            try:
                books, soup = scrape_page(session, current_url)
            except requests.RequestException as error:
                print(f"Could not fetch page {page_number}: {error}")
                break
            all_books.extend(books)
            next_link = soup.select_one("li.next a")
            if not next_link:
                break
            current_url = urljoin(current_url, next_link.get("href", ""))
            time.sleep(1)
    if not all_books:
        print("No books collected. Check internet connection and try again.")
        return
    df = pd.DataFrame(all_books).drop_duplicates(subset=["product_url"])
    csv_path = output_dir / "books.csv"
    df.to_csv(csv_path, index=False, encoding="utf-8-sig")
    print(f"Saved {len(df)} books to: {csv_path.resolve()}")
    print(df.head(10).to_string(index=False))

if __name__ == "__main__":
    main()
