import argparse
import csv
from bol_scraper import scrape_bol_category
from amazon_scraper import search_amazon_de
from scorer import score_gap

# Known bol.com category URLs
CATEGORY_URLS = {
    "home-decor":   "https://www.bol.com/nl/nl/l/woonaccessoires/",
    "kitchen":      "https://www.bol.com/nl/nl/l/keuken/",
    "textiles":     "https://www.bol.com/nl/nl/l/beddengoed/",
}


def run(category: str, min_reviews: int, max_results: int, output_file: str):
    category_url = CATEGORY_URLS.get(category)
    if not category_url:
        print(f"Unknown category: {category}. Options: {list(CATEGORY_URLS.keys())}")
        return

    print(f"Scraping bol.com category: {category}")
    products = scrape_bol_category(category_url, max_pages=5)
    print(f"Found {len(products)} products on bol.com")

    results = []
    for p in products:
        if p["bol_reviews"] < min_reviews:
            continue

        print(f"  Checking Amazon.de for: {p['title'][:50]}...")
        amazon = search_amazon_de(p["title"])

        gap_score = score_gap(
            p["bol_reviews"], p["bol_price"],
            amazon["found"], amazon.get("price")
        )

        results.append({
            "title":           p["title"],
            "bol_price":       p["bol_price"],
            "bol_reviews":     p["bol_reviews"],
            "bol_url":         p["bol_url"],
            "amazon_de_found": amazon["found"],
            "amazon_de_price": amazon.get("price"),
            "amazon_asin":     amazon.get("asin"),
            "gap_score":       gap_score,
        })

    # Sort by gap score descending
    results.sort(key=lambda x: x["gap_score"], reverse=True)
    results = results[:max_results]

    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)

    print(f"\nTop {len(results)} opportunities saved to {output_file}")
    print("\nTop 5 preview:")
    for r in results[:5]:
        amazon_str = f"€{r['amazon_de_price']:.2f}" if r["amazon_de_price"] else "Not listed"
        print(f"  [{r['gap_score']}] {r['title'][:45]}... | bol: €{r['bol_price']} | amazon.de: {amazon_str}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--category",    default="home-decor", choices=list(CATEGORY_URLS.keys()))
    parser.add_argument("--min-reviews", type=int, default=50)
    parser.add_argument("--max-results", type=int, default=100)
    parser.add_argument("--output",      default="gap_results.csv")
    args = parser.parse_args()

    run(args.category, args.min_reviews, args.max_results, args.output)
