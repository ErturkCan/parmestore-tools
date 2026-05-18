def check_threshold(current_price: float, threshold: float, product_name: str) -> bool:
    if current_price is None:
        return False
    if current_price <= threshold:
        print(f"[ALERT] '{product_name}' dropped to €{current_price:.2f} (threshold: €{threshold:.2f})")
        return True
    return False
