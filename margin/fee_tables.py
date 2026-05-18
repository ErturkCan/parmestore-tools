# Marketplace commission rates as of 2025
# Sources: bol.com partner API docs, Amazon Seller Central DE

BOL_FEES = {
    "home_decor":      0.15,
    "kitchen":         0.15,
    "textiles":        0.13,
    "electronics":     0.10,
    "toys":            0.15,
    "default":         0.15,
}

AMAZON_DE_FEES = {
    "home_decor":      0.15,
    "kitchen":         0.15,
    "textiles":        0.15,
    "electronics":     0.08,
    "toys":            0.15,
    "default":         0.15,
}

# Fixed per-item fulfillment costs (FBM estimate, own warehouse)
FULFILLMENT_COST = {
    "bol":       1.80,
    "amazon_de": 2.20,
}

VAT_RATES = {
    "NL": 0.21,
    "DE": 0.19,
    "BE": 0.21,
}
