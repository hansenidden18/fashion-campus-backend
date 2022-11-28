def regular_fee(price):
    if price < 200_000:
        return 0.15 * price
    else:
        return 0.2 * price

def next_fee(price):
    if price < 300_000:
        return 0.2 * price
    else:
        return 0.25 * price