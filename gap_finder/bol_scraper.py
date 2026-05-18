import time
import random
import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}


def scrape_bol_category(category_url: str, max_pages: int = 3) -> list[dict]:
    products = []

    for page in range(1, max_pages + 1):
        url = f"{category_url}?page={page}"
        try:
            resp = requests.get(url, headers=HEADERS, timeout=10)
            resp.raise_for_status()
        except requests.RequestException as e:
            print(f"Error on page {page}: {e}")
            break

        soup = BeautifulSoup(resp.text, "html.parser")
        items = soup.select("li[data-test='product-item']")

        if not items:
            break

        for item in items:
            title_tag = item.select_one("[data-test='product-title']")
            price_tag = item.select_one("[data-test='price']")
            reviews_tag = item.select_one("[data-test='review-count']")
            link_tag = item.select_one("a[data-test='product-link']")

            title = title_tag.get_text(strip=True) if title_tag else None
            link  = "https://www.bol.com" + link_tag["href"] if link_tag else None

            price = None
            if price_tag:
                try:
                    price = float(price_tag.get_text(strip=True)
                                  .replace("€", "").replace(",", ".").strip())
                except ValueError:
                    pass

            reviews = 0
            if reviews_tag:
                try:
                    reviews = int(reviews_tag.get_text(strip=True)
                                  .replace("(", "").replace(")", "").replace(".", "").strip())
                except ValueError:
                    pass

            if title and link:
                products.append({
                    "title": title,
                    "bol_price": price,
                    "bol_reviews": reviews,
                    "bol_url": link,
                })

        time.sleep(random.uniform(1.5, 3.0))

    return products
