import time
import random
import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}


def _get(url, retries=3):
    for attempt in range(retries):
        try:
            resp = requests.get(url, headers=HEADERS, timeout=10)
            resp.raise_for_status()
            return resp
        except requests.RequestException as e:
            if attempt == retries - 1:
                raise
            time.sleep(2 ** attempt)


def fetch_bol_price(product_url: str) -> dict:
    resp = _get(product_url)
    soup = BeautifulSoup(resp.text, "html.parser")

    price = None
    title = None

    # Try main price selector
    price_tag = soup.select_one("[data-test='price']")
    if price_tag:
        raw = price_tag.get_text(strip=True).replace("€", "").replace(",", ".").strip()
        try:
            price = float(raw)
        except ValueError:
            pass

    title_tag = soup.select_one("h1[data-test='title']")
    if title_tag:
        title = title_tag.get_text(strip=True)

    return {"platform": "bol", "url": product_url, "title": title, "price": price}


def fetch_amazon_de_price(product_url: str) -> dict:
    resp = _get(product_url)
    soup = BeautifulSoup(resp.text, "html.parser")

    price = None
    title = None

    # Amazon price is split across two spans: whole and fraction
    whole = soup.select_one("span.a-price-whole")
    fraction = soup.select_one("span.a-price-fraction")
    if whole and fraction:
        try:
            price = float(whole.get_text(strip=True).replace(".", "").replace(",", "")
                          + "." + fraction.get_text(strip=True))
        except ValueError:
            pass

    title_tag = soup.select_one("#productTitle")
    if title_tag:
        title = title_tag.get_text(strip=True)

    return {"platform": "amazon_de", "url": product_url, "title": title, "price": price}
