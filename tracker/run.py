import argparse
import csv
import time
import random
from fetcher import fetch_bol_price, fetch_amazon_de_price
from storage import init_db, save_price
from alerts import check_threshold


def load_watchlist(path: str) -> list[dict]:
    products = []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            products.append(row)
    return products


def run(watchlist_path: str, interval_seconds: int):
    init_db()
    products = load_watchlist(watchlist_path)
    print(f"Loaded {len(products)} products. Checking every {interval_seconds}s.")

    while True:
        for p in products:
            url = p["url"]
            platform = p.get("platform", "bol")
            threshold = float(p.get("alert_threshold", 0))

            try:
                if platform == "bol":
                    record = fetch_bol_price(url)
                elif platform == "amazon_de":
                    record = fetch_amazon_de_price(url)
                else:
                    print(f"Unknown platform: {platform}")
                    continue

                save_price(record)
                price_str = f"€{record['price']:.2f}" if record["price"] else "N/A"
                print(f"[{platform}] {record['title'][:50]}... → {price_str}")

                if threshold > 0:
                    check_threshold(record["price"], threshold, record["title"])

            except Exception as e:
                print(f"Error fetching {url}: {e}")

            # Random delay between requests to avoid rate limiting
            time.sleep(random.uniform(2, 5))

        print(f"\nCycle done. Sleeping {interval_seconds}s...\n")
        time.sleep(interval_seconds)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--products", default="data/watchlist.csv")
    parser.add_argument("--interval", type=int, default=3600, help="Seconds between full cycles")
    args = parser.parse_args()
    run(args.products, args.interval)
