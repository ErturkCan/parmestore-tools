import csv
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import requests
from margin.calculate import calculate_margin
from gap_finder.scan import run
from gap_finder.amazon_scraper import search_amazon_de


class ToolTests(unittest.TestCase):
    def test_margin_accounts_for_inclusive_vat_and_costs(self):
        result = calculate_margin(4.50, 1.20, 18.99, "bol")
        self.assertAlmostEqual(result["net_margin_eur"], 5.34)
        self.assertAlmostEqual(result["vat"], 3.30)
        self.assertEqual(result["margin_pct"], 28.1)

    def test_module_entrypoints_load(self):
        for module in ("margin.calculate", "tracker.run", "gap_finder.scan"):
            result = subprocess.run([sys.executable, "-m", module, "--help"], capture_output=True)
            self.assertEqual(result.returncode, 0, result.stderr.decode())

    def test_empty_scan_writes_header(self):
        with tempfile.TemporaryDirectory() as d, patch("gap_finder.scan.scrape_bol_category", return_value=[]):
            out = Path(d) / "results.csv"
            run("kitchen", 50, 10, str(out))
            with out.open() as f:
                reader = csv.DictReader(f)
                self.assertIn("gap_score", reader.fieldnames)
                self.assertEqual(list(reader), [])

    def test_http_failure_is_unknown_not_missing_listing(self):
        with patch("gap_finder.amazon_scraper.requests.get", side_effect=requests.Timeout):
            self.assertIsNone(search_amazon_de("example")["found"])

    def test_failed_lookup_is_not_ranked(self):
        products = [{"title": "Example", "bol_reviews": 200, "bol_price": 25, "bol_url": "example"}]
        with tempfile.TemporaryDirectory() as d, patch("gap_finder.scan.scrape_bol_category", return_value=products), patch("gap_finder.scan.search_amazon_de", return_value={"found": None}):
            out = Path(d) / "results.csv"
            run("kitchen", 50, 10, str(out))
            with out.open() as f:
                self.assertEqual(list(csv.DictReader(f)), [])
