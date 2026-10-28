# CodeAlpha Task 1 — Web Scraping

## Objective
Collect book title, price, availability, rating, and product page URL from the public practice website Books to Scrape.

## Setup
```bash
python -m pip install -r requirements.txt
python scraper.py
```
The script visits up to 3 pages, waits briefly between requests, and saves data to `output/books.csv`.

## Output columns
`title`, `price_gbp`, `availability`, `rating`, `product_url`, `source_page`

## Responsible scraping
This project uses a practice website intended for scraping exercises. Keep request volume low, use delays, and check a website's terms and robots.txt before scraping other sites.
