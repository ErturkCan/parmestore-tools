import argparse
from fee_tables import BOL_FEES, AMAZON_DE_FEES, FULFILLMENT_COST
from vat import calculate_vat, price_excl_vat


def calculate_margin(
    wholesale_eur: float,
    shipping_eur: float,
    sale_price: float,
    marketplace: str,
    category: str = "default",
    country: str = "NL",
) -> dict:
    marketplace = marketplace.lower()

    if marketplace == "bol":
        fee_rate = BOL_FEES.get(category, BOL_FEES["default"])
    elif marketplace == "amazon_de":
        fee_rate = AMAZON_DE_FEES.get(category, AMAZON_DE_FEES["default"])
        country = "DE"
    else:
        raise ValueError(f"Unknown marketplace: {marketplace}")

    marketplace_fee = round(sale_price * fee_rate, 2)
    fulfillment    = FULFILLMENT_COST.get(marketplace, 2.00)
    vat            = calculate_vat(sale_price, country)
    total_cost     = round(wholesale_eur + shipping_eur + marketplace_fee + fulfillment, 2)
    net_revenue    = round(price_excl_vat(sale_price, country) - marketplace_fee - fulfillment, 2)
    net_margin     = round(net_revenue - wholesale_eur - shipping_eur, 2)
    margin_pct     = round((net_margin / sale_price) * 100, 1) if sale_price > 0 else 0

    return {
        "wholesale":        wholesale_eur,
        "shipping":         shipping_eur,
        "marketplace_fee":  marketplace_fee,
        "fulfillment":      fulfillment,
        "vat":              vat,
        "total_cost":       total_cost,
        "sale_price":       sale_price,
        "net_margin_eur":   net_margin,
        "margin_pct":       margin_pct,
    }


def print_result(r: dict):
    print(f"\n{'─'*35}")
    print(f"  Wholesale:         €{r['wholesale']:.2f}")
    print(f"  Shipping:          €{r['shipping']:.2f}")
    print(f"  Marketplace fee:   €{r['marketplace_fee']:.2f}")
    print(f"  Fulfillment:       €{r['fulfillment']:.2f}")
    print(f"  VAT (in price):    €{r['vat']:.2f}")
    print(f"{'─'*35}")
    print(f"  Total cost:        €{r['total_cost']:.2f}")
    print(f"  Sale price:        €{r['sale_price']:.2f}")
    print(f"  Net margin:        €{r['net_margin_eur']:.2f}  ({r['margin_pct']}%)")
    print(f"{'─'*35}\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Calculate net margin for a product")
    parser.add_argument("--wholesale",   type=float, required=True, help="China wholesale price in EUR")
    parser.add_argument("--shipping",    type=float, required=True, help="Shipping cost per unit in EUR")
    parser.add_argument("--sale-price",  type=float, required=True, help="Listed sale price in EUR")
    parser.add_argument("--marketplace", required=True, choices=["bol", "amazon_de"])
    parser.add_argument("--category",    default="default", help="Product category for fee lookup")
    parser.add_argument("--country",     default="NL", help="Country for VAT calculation")
    args = parser.parse_args()

    result = calculate_margin(
        args.wholesale, args.shipping, args.sale_price,
        args.marketplace, args.category, args.country
    )
    print_result(result)
