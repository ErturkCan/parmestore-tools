# Parmestore tools

Small Python tools for questions I dealt with through Parmestore: what is left after costs, how prices move, and which listings are worth looking into. Parmestore closed in November 2025; this repository is a collection of tools and experiments around that work.

## Start with the margin calculator

This command uses only the Python standard library:

```bash
python -m margin.calculate --wholesale 4.50 --shipping 1.20 --sale-price 18.99 --marketplace bol
```

It separates VAT included in the sale price, marketplace commission, fulfilment, wholesale and shipping. The fee tables are illustrative assumptions, not current marketplace quotations or a complete tax model. Check and adjust `margin/fee_tables.py` before using the output for a business decision.

## Price tracking and listing comparison

From the repository root, with Python 3.10 or later:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m tracker.run --products data/watchlist.csv --interval 3600
python -m gap_finder.scan --category kitchen --min-reviews 50 --max-results 20 --output gap_results.csv
```

Replace the sample watchlist with listings you want to check. The tracker stores observations in `data/prices.db` and prints threshold alerts. The scanner compares bol.com listings with the first Amazon.de search result and writes a ranked CSV.

The HTML selectors can stop working when a site changes or blocks a request. A missing search result is not proof of a market gap, and the first result may be a different product. Scores are a rough review order, not validated demand estimates. These commands make live web requests; the tests below do not.

## Layout

- `margin/`: cost calculation and example fee/VAT tables.
- `tracker/`: fetchers, SQLite history and console alerts.
- `gap_finder/`: listing search and a simple scoring rule.
- `config/config.example.toml`: example settings; the CLI currently takes arguments directly and does not load this file.

```bash
python -m unittest discover -s tests -v
```
