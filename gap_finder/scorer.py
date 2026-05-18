def score_gap(bol_reviews: int, bol_price: float, amazon_found: bool, amazon_price: float) -> float:
    score = 0.0

    # More bol reviews = stronger proven demand
    if bol_reviews >= 200:
        score += 40
    elif bol_reviews >= 50:
        score += 20
    elif bol_reviews >= 10:
        score += 10

    # Not on Amazon DE = clear gap
    if not amazon_found:
        score += 40
    elif amazon_price and bol_price:
        # Present on Amazon but priced higher = opportunity to undercut
        if amazon_price > bol_price * 1.15:
            score += 20

    # Higher price products have better absolute margin potential
    if bol_price and bol_price >= 25:
        score += 20
    elif bol_price and bol_price >= 15:
        score += 10

    return round(score, 1)
