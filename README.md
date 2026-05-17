# parmestore-tools

Automation suite for [Parmestore International](https://linkedin.com/in/canetrk) — a KVK-registered China-Europe e-commerce company.

Tools for price tracking, margin calculation, and cross-platform product gap finding across bol.com and Amazon.de.

---

## What this is

Parmestore is my company. I source products directly from China and sell across European marketplaces. Managing pricing, margins, and product opportunities manually doesn't scale — so I built tools.

This repo contains the automation scripts I actually use to run the business.

---

## Tools

### 1. Price Tracker (`tracker/`)

Monitors competitor prices on bol.com and Amazon.de for a given product list. Logs price changes and alerts when a target product drops below a threshold.

```bash
python tracker/run.py --products data/watchlist.csv --interval 3600
```

**What it does:**
- Fetches current prices from bol.com and Amazon.de product pages
- Logs to SQLite with timestamp
- Outputs daily price change summary
- Configurable alert threshold per product

---

### 2. Margin Calculator (`margin/`)

Given a product's China wholesale price, shipping cost, and target marketplace, calculates landed cost, marketplace fees, VAT, and net margin.

```bash
python margin/calculate.py --wholesale 4.50 --shipping 1.20 --marketplace bol --sale-price 19.99
```

**Output:**
```
Product Cost:     €4.50
Shipping:         €1.20
Marketplace fee:  €3.00  (15%)
VAT (21%):        €3.47
─────────────────────────
Total cost:       €8.17
Sale price:       €19.99
Net margin:       €11.82  (59.1%)
```

Supports: bol.com, Amazon.de, Amazon.nl fee structures.

---

### 3. Product Gap Finder (`gap_finder/`)

Cross-references top-selling products on bol.com against Amazon.de listings. Finds products with strong bol.com demand but weak or no Amazon.de presence — potential white space opportunities.

```bash
python gap_finder/scan.py --category "home-decor" --min-reviews 50 --max-results 100
```

**Output:** CSV with columns: product, bol_rank, bol_reviews, bol_price, amazon_de_present, amazon_de_price, gap_score

---

## Setup

```bash
git clone https://github.com/ErturkCan/parmestore-tools
cd parmestore-tools
pip install -r requirements.txt
cp config/config.example.toml config/config.toml
# Edit config.toml with your settings
```

**Requirements:** Python 3.10+, requests, BeautifulSoup4, pandas, sqlite3, rich, toml

---

## Project Structure

```
parmestore-tools/
├── tracker/
│   ├── run.py              # Main price tracking loop
│   ├── fetcher.py          # bol.com + Amazon.de scrapers
│   ├── storage.py          # SQLite logging
│   └── alerts.py           # Threshold alerting
├── margin/
│   ├── calculate.py        # CLI margin calculator
│   ├── fee_tables.py       # Marketplace fee structures
│   └── vat.py              # VAT calculation by country
├── gap_finder/
│   ├── scan.py             # Main gap finder script
│   ├── bol_scraper.py      # bol.com category scraper
│   ├── amazon_scraper.py   # Amazon.de lookup
│   └── scorer.py           # Gap scoring logic
├── data/
│   ├── watchlist.csv       # Example product watchlist
│   └── fee_structures/     # Fee tables per marketplace
├── config/
│   └── config.example.toml
├── notebooks/
│   └── margin_analysis.ipynb  # Historical margin analysis
├── requirements.txt
└── README.md
```

---

## Context

**Parmestore International** is a KVK-registered e-commerce company (Netherlands) I founded before starting university. We source home decor, kitchen accessories, and textiles directly from Chinese suppliers and sell on European marketplaces. Currently generating €550+/month, expanding to bol.com and Amazon.de. Attending Canton Fair Guangzhou October–November 2026 for direct supplier sourcing.

These tools exist because running arbitrage and sourcing decisions manually at scale is not feasible. The automation saves roughly 3–4 hours per week and reduces pricing errors.

---

## Notes on scraping

The scrapers respect rate limits and use randomized delays. They are for personal/business use on publicly visible prices — not for resale or bulk data extraction. If you use this, be responsible.

---

## License

MIT
