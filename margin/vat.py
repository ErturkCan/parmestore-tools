from fee_tables import VAT_RATES


def calculate_vat(sale_price: float, country: str = "NL") -> float:
    rate = VAT_RATES.get(country.upper(), 0.21)
    # VAT is already included in the sale price (Dutch/EU standard)
    vat_amount = sale_price - (sale_price / (1 + rate))
    return round(vat_amount, 2)


def price_excl_vat(sale_price: float, country: str = "NL") -> float:
    rate = VAT_RATES.get(country.upper(), 0.21)
    return round(sale_price / (1 + rate), 2)
