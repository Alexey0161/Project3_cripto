import sys
import sqlite3
from selenium import webdriver
from selenium.webdriver.common.by import By # Помогает искать элементы
import time
from datetime import datetime # Импортируем время
from  logic.insert_to_db import insert_to_db
from  logic.clean_name import clean_name
from logic.clean_price import clean_price


def run_crypto_scraper():
    driver = webdriver.Chrome()

    ### 1. Вариант для всей таблицы
    try:
        driver.get("https://coinmarketcap.com/")
        time.sleep(3) # Ждем чуть дольше для JS
    except Exception as e:
        print(f"Ошибка: {e}")
        # 1. Сначала находим все строки таблицы (Rows)
    # Мы используем find_elements (во множественном числе!), чтобы получить список
    # Селектор "tbody tr" говорит: "найди все строки внутри тела таблицы"
    rows = driver.find_elements(By.CSS_SELECTOR, "table.cmc-table tbody tr")

    # 2. Запускаем цикл по первым 10 строкам
    for row in rows[:5]:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            # ВАЖНО: ищем ВНУТРИ текущей строки row (ставим row. перед find_element)
            
            # используем номер столбца, в котором лежит название крипты
            name = row.find_element(By.CSS_SELECTOR, "td:nth-child(3)").text
            name_clean = clean_name(name)
        
            price = row.find_element(By.CSS_SELECTOR, 'div [class*="sc-"] >span').text
            price = clean_price(price)
            
            print("Скрапинг завершен успешно!")
            # print(f"Крипта: {name} | Цена: {price} | {current_time}")
            insert_to_db(name_clean, price, current_time)
        except Exception as e:
            print(f'Ошибка: {e}')
            # Если в строке реклама или она пустая — просто идем дальше
            continue

if __name__ == "__main__":
    run_crypto_scraper()