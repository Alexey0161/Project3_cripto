def clean_ticker(name):
    ind1 = name.rfind('\n')
    name_1 = name[ :ind1]
    ind2 = name_1.rfind('\n')
    ticker = name_1[ind2+1 :]
    return ticker
    # d = name.split('\n')
    # return d

# print(clean_ticker('Bitcoin BTC Buy'))