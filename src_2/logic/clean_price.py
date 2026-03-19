def clean_price(price):
    if price:
        price = price[1:]
        price = price.replace(',', '.')
        # print(price)
        price = price.split('.')
        price = price[0] + '.' + ''.join(price[1:])
        return float(price)
    else:
        return 0

# print(clean_price('$34,45,245,452,452,4'))