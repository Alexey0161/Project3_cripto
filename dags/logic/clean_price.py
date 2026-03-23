def clean_price(price):
    if not price:
        return 0
    # Просто убираем ВСЁ, кроме цифр и точки
    clean_val = price.replace("$", "").replace(",", "")
    return float(clean_val)
