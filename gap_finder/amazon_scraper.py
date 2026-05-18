import time
import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}


def search_amazon_de(query: str) -> dict:
    search_url = f"https://www.amazon.de/s?k={requests.utils.quote(query)}"
    try:
        resp = requests.get(search_url, headers=HEADERS, timeout=10)
        resp.raise_for_status()
    except requests.RequestException:
        return {"found": False, "price": None, "asin": None}

    soup = BeautifulSoup(resp.text, "html.parser")

    # Take the first organic result
    result = soup.select_one("[data-component-type='s-search-result']")
    if not result:
        return {"found": False, "price": None, "asin": None}

    asin = result.get("data-asin")

    price = None
    whole = result.select_one("span.a-price-whole")
    fraction = result.select_one("span.a-price-fraction")
    if whole and fraction:
        try:
            price = float(
                whole.get_text(strip=True).replace(".", "").replace(",", "")
                + "." + fraction.get_text(strip=True)
            )
        except ValueError:
            pass

    time.sleep(2)
    return {"found": True, "price": price, "asin": asin}
