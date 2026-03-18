import sys
import sqlite3
from selenium import webdriver
from selenium.webdriver.common.by import By # Помогает искать элементы
import time
driver = webdriver.Chrome()
##### 1.  Вариант для Биткоина на его именной странице <---- описан процесс обучения поиску
# try:
#     # driver.get("https://coinmarketcap.com/")
#     driver.get("https://coinmarketcap.com/currencies/bitcoin/")
#     time.sleep(3) # Ждем чуть дольше для JS

#     # 1. Ищем название (оно обычно в <h1> или крупном <span>)
#     # На CoinMarketCap название монеты часто имеет класс 'coin-name-mobile' или просто лежит в h1
#     name = driver.find_element(By.TAG_NAME, "h1").text
    
#     # 2. Ищем цену (используем более точный селектор)
#     # Посмотрим в F12, там у цены должен быть класс типа "fs-2" или "priceValue"
#     # Для примера возьмем селектор по классу (он может меняться, проверьте в F12!)
#     
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

# 2. Запускаем цикл по первым 10 строкам
for row in rows[:5]:
    
    try:
        # ВАЖНО: ищем ВНУТРИ текущей строки row (ставим row. перед find_element)
        
        # Ищем название (используем название класса, которое нашли в F12)
        # name = row.find_element(By.CSS_SELECTOR, ".coin-item-name").text
        # используем номер столбца, в котором лежит название крипты
        name = row.find_element(By.CSS_SELECTOR, "td:nth-child(3)").text
    
        
        # ищем от тега div до span, дополнительное условие, что в строке должно быть
        ### название класса, у которого первые буквы sc, так как класс динамический, то цифры
        #### могут меняться но через *= мы найдем название класса в котором зашит текст цены
        ##### а далее через метед CSS-селектора - .text мы находим текст, а это и есть цена в строковом виде.
        ###### потому что мы знаем, что все буквенные или цифровые символы разработчики делают типа text
        # price = row.find_element(By.CSS_SELECTOR, 'div[class*="sc-"] > span').text
        # price = row.find_element(By.CSS_SELECTOR, 'td:nth-child(4)').text
        price = row.find_element(By.CSS_SELECTOR, 'div [class*="sc-"] >span').text
 
        
        print(f"Крипта: {name} | Цена: {price}")
        
    except Exception as e:
        print(f'Ошибка: {e}')
        # Если в строке реклама или она пустая — просто идем дальше
        continue

