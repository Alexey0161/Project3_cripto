import sys
import sqlite3
from selenium import webdriver
from selenium.webdriver.common.by import By # Помогает искать элементы
import time
driver = webdriver.Chrome()
##### 1.  Вариант для Биткоина на его именной странице
# try:
#     # driver.get("https://coinmarketcap.com/")
#     driver.get("https://coinmarketcap.com/currencies/bitcoin/")
#     time.sleep(3) # Ждем чуть дольше для JS

#     # 1. Ищем название (оно обычно в <h1> или крупном <span>)
#     # На CoinMarketCap название монеты часто имеет класс 'coin-name-mobile' или просто лежит в h1
#     name = driver.find_element(By.TAG_NAME, "h1").text
    
#     # 2. Ищем цену (используем более точный селектор)
#     # Посмотрите в F12, там у цены должен быть класс типа "fs-2" или "priceValue"
#     # Для примера возьмем селектор по классу (он может меняться, проверьте в F12!)
#     # price = driver.find_element(By.CSS_SELECTOR, "<span>$73,774.41</span>").text
#     # Мы ищем тег span, у которого есть класс, отвечающий за цену
# # На CoinMarketCap это часто динамические классы, но можно зацепиться за общие
#     # price=driver.find_element(By.CSS_SELECTOR,'[class*="price"]').text
#     price=driver.find_element(By.CSS_SELECTOR,'#section-coin-overview > div.sc-c1554bc0-0.efjLyZ.flexStart.alignBaseline > span').text
#     print(f"Валюта: {name}")
#     print(f"Текущая цена: {price}")

# except Exception as e:
#     print(f"Ой, Техлид, у нас проблема: {e}")

### 2. Вариант для всей таблицы
try:
    driver.get("https://coinmarketcap.com/")
    # driver.get("https://coinmarketcap.com/currencies/bitcoin/")
    time.sleep(3) # Ждем чуть дольше для JS
except Exception as e:
    print(f"Ой, Техлид, у нас проблема: {e}")
    # 1. Сначала находим все строки таблицы (Rows)
# Мы используем find_elements (во множественном числе!), чтобы получить список
# Селектор "tbody tr" говорит: "найди все строки внутри тела таблицы"
rows = driver.find_elements(By.CSS_SELECTOR, "table.cmc-table tbody tr")

print(f"Вижу строк в таблице: {len(rows)}")

# 2. Запускаем цикл по первым 10 строкам
for row in rows[:5]:
    # print(row, 47)
    try:
        # ВАЖНО: ищем ВНУТРИ текущей строки row (ставим row. перед find_element)
        
        # Ищем название (используйте тот селектор, что нашли в F12)
        name = row.find_element(By.CSS_SELECTOR, ".coin-item-name").text
        # print(name, 53)
        
        # Ищем цену (используем ваш 'data-test' или класс из шага с ценой)
        # На главной это часто просто ячейка с классом, содержащим 'price'
        # price = row.find_element(By.CSS_SELECTOR, 'div[class*="sc-"] > span').text
        # price = row.find_element(By.CSS_SELECTOR, 'td:nth-child(4)').text
        price = row.find_element(By.CSS_SELECTOR, 'div [class*="sc-"] >span').text
        # price = row.find_element(By.CSS_SELECTOR, "#section-coin-overview > div.sc-c1554bc0-0.efjLyZ.flexStart.alignBaseline > span").text
        # print(price, 58)
        
        print(f"Крипта: {name} | Цена: {price}")
        
    except Exception as e:
        print(f'Ошибка: {e}')
        # Если в строке реклама или она пустая — просто идем дальше
        continue
#     # 1. Ищем название (оно обычно в <h1> или крупном <span>)
#     # На CoinMarketCap название монеты часто имеет класс 'coin-name-mobile' или просто лежит в h1
#     name = driver.find_element(By.TAG_NAME, "h1").text
    
#__next > div.sc-2e4c98e0-1.hYcKwZ.global-layout-v2 > div.main-content > div.cmc-body-wrapper > div > div.sc-6f9d27dc-2.laUnld > div > div:nth-child(5) > div.sc-7e3c705d-2.mJVuU > table > tbody > tr:nth-child(1)