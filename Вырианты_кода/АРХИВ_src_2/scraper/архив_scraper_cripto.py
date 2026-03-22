import os
import sys
# Добавляем ПУТЬ К ПАПКЕ src_2 в систему поиска Python
# В контейнере это /opt/airflow/src_2
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

import sqlite3
from selenium import webdriver
from selenium.webdriver.common.by import By # Помогает искать элементы
from selenium.webdriver.chrome.options import Options
import time
from datetime import datetime # Импортируем время
from  logic.insert_to_db import insert_to_db
from  logic.clean_name import clean_name
from logic.clean_price import clean_price


def run_crypto_scraper():
    print("--- DEBUG INFO START ---")
    print(f"Текущая рабочая директория (CWD): {os.getcwd()}")
    print(f"Список файлов в /opt/airflow/: {os.listdir('/opt/airflow/')}")
    # Проверяем, видит ли он нашу папку src_2
    if os.path.exists('/opt/airflow/src_2'):
        print(f"✅ Папка src_2 найдена! Содержимое: {os.listdir('/opt/airflow/src_2')}")
    else:
        print("❌ ОШИБКА: Папка /opt/airflow/src_2 НЕ НАЙДЕНА!")
    print("--- DEBUG INFO END ---")
    
    options = Options()
    # options = webdriver.ChromeOptions()
    options.add_argument("--headless")        # Самое важное! Без окна
    options.add_argument("--no-sandbox")       # Для работы в Docker
    options.add_argument("--disable-dev-shm-usage") 

    # driver = webdriver.Chrome(options=options)
    # ВАЖНО: Подключаемся к удаленному браузеру в соседнем контейнере
    print("🌐 Подключаюсь к удаленному Selenium Grid...")
    driver = webdriver.Remote(
        command_executor='http://selenium-chrome:4444/wd/hub',
        options=options
    )
    
    print("🚀 Старт скрапера...")
    ### 1. Вариант для всей таблицы
    try:
        print("🌐 Пытаюсь открыть сайт...")
        driver.get("https://coinmarketcap.com/")
        time.sleep(3) # Ждем чуть дольше для JS
    except Exception as e:
        print(f"Ошибка: {e}")
        # 1. Сначала находим все строки таблицы (Rows)
    # Мы используем find_elements (во множественном числе!), чтобы получить список
    # Селектор "tbody tr" говорит: "найди все строки внутри тела таблицы"
    rows = driver.find_elements(By.CSS_SELECTOR, "table.cmc-table tbody tr")
    if not rows:
            print("⚠️ Внимание: Данные не найдены на странице!")
    else:
            print(f"✅ Собрано {len(rows)} строк данных.")
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
            # print(f"💾 Подключаюсь к базе по пути: {os.path.abspath('crypto_data.db')}")
            insert_to_db(name_clean, price, current_time)
        except Exception as e:
            print(f"❌ Произошла ошибка: {str(e)}")
            raise e # Важно пробросить ошибку вверх, чтобы Airflow её увидел
            # Если в строке реклама или она пустая — просто идем дальше
            continue

if __name__ == "__main__":
    run_crypto_scraper()