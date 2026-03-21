# import os
# import sys
# # Добавляем ПУТЬ К ПАПКЕ src_2 в систему поиска Python
# # В контейнере это /opt/airflow/src_2
# current_dir = os.path.dirname(os.path.abspath(__file__))
# if current_dir not in sys.path:
#     sys.path.append(current_dir)

# from airflow import DAG
# from airflow.operators.python import PythonOperator
# import sqlite3
# from selenium import webdriver
# from selenium.webdriver.common.by import By # Помогает искать элементы
# from selenium.webdriver.chrome.options import Options
# import time
# from datetime import datetime, timedelta # Импортируем время
# from  logic.insert_to_db import insert_to_db
# from  logic.clean_name import clean_name
# from logic.clean_price import clean_price

# default_args = {
#     'owner': 'airflow',
#     'depends_on_past': False,
#     'start_date': datetime(2026, 3, 20), # Вчерашняя дата, чтобы он сразу захотел запуститься
#     'retries': 1,
#     'retry_delay': timedelta(minutes=5),
# }

# with DAG(
#     'crypto_market_scraper_v1', # Вот это имя появится в списке!
#     default_args=default_args,
#     description='My beautiful crypto scraper',
#     schedule_interval=timedelta(days=1), # Тот самый schedule!
#     catchup=False
# ) as dag:

#     def run_crypto_scraper():
#         print("--- DEBUG INFO START ---")
#         print(f"Текущая рабочая директория (CWD): {os.getcwd()}")
#         print(f"Список файлов в /opt/airflow/: {os.listdir('/opt/airflow/')}")
#         # Проверяем, видит ли он нашу папку src_2
#         if os.path.exists('/opt/airflow/src_2'):
#             print(f"✅ Папка src_2 найдена! Содержимое: {os.listdir('/opt/airflow/src_2')}")
#         else:
#             print("❌ ОШИБКА: Папка /opt/airflow/src_2 НЕ НАЙДЕНА!")
#         print("--- DEBUG INFO END ---")
        
#         options = Options()
#         # options = webdriver.ChromeOptions()
#         options.add_argument("--headless")        # Самое важное! Без окна
#         options.add_argument("--no-sandbox")       # Для работы в Docker
#         options.add_argument("--disable-dev-shm-usage") 

#         # driver = webdriver.Chrome(options=options)
#         # ВАЖНО: Подключаемся к удаленному браузеру в соседнем контейнере
#         print("🌐 Подключаюсь к удаленному Selenium Grid...")
#         driver = webdriver.Remote(
#             command_executor='http://selenium-chrome:4444/wd/hub',
#             options=options
#         )
        
#         print("🚀 Старт скрапера...")
#         ### 1. Вариант для всей таблицы
#         try:
#             print("🌐 Пытаюсь открыть сайт...")
#             driver.get("https://coinmarketcap.com/")
#             time.sleep(3) # Ждем чуть дольше для JS
#         except Exception as e:
#             print(f"Ошибка: {e}")
#             # 1. Сначала находим все строки таблицы (Rows)
#         # Мы используем find_elements (во множественном числе!), чтобы получить список
#         # Селектор "tbody tr" говорит: "найди все строки внутри тела таблицы"
#         rows = driver.find_elements(By.CSS_SELECTOR, "table.cmc-table tbody tr")
#         if not rows:
#                 print("⚠️ Внимание: Данные не найдены на странице!")
#         else:
#                 print(f"✅ Собрано {len(rows)} строк данных.")
#         # 2. Запускаем цикл по первым 10 строкам
#         for row in rows[:5]:
#             current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#             try:
#                 # ВАЖНО: ищем ВНУТРИ текущей строки row (ставим row. перед find_element)
                
#                 # используем номер столбца, в котором лежит название крипты
#                 name = row.find_element(By.CSS_SELECTOR, "td:nth-child(3)").text
#                 name_clean = clean_name(name)
            
#                 price = row.find_element(By.CSS_SELECTOR, 'div [class*="sc-"] >span').text
#                 price = clean_price(price)
                
#                 print("Скрапинг завершен успешно!")
#                 # print(f"Крипта: {name} | Цена: {price} | {current_time}")
#                 # print(f"💾 Подключаюсь к базе по пути: {os.path.abspath('crypto_data.db')}")
#                 insert_to_db(name_clean, price, current_time)
#             except Exception as e:
#                 print(f"❌ Произошла ошибка: {str(e)}")
#                 raise e # Важно пробросить ошибку вверх, чтобы Airflow её увидел
#                 # Если в строке реклама или она пустая — просто идем дальше
#                 continue

# if __name__ == "__main__":
#     run_crypto_scraper()

import os
import sys
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'libs'))
from datetime import datetime, timedelta # ИСПРАВЛЕНО: добавили timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator
# Определяем путь к папке dags
dags_folder = os.path.dirname(__file__)

# Добавляем путь к библиотекам libs
libs_path = os.path.join(dags_folder, 'libs')
if libs_path not in sys.path:
    sys.path.insert(0, libs_path)

# Добавляем путь к папке logic (она же у вас в dags лежит?)
if dags_folder not in sys.path:
    sys.path.insert(0, dags_folder)
# Эти импорты могут подчеркиваться желтым в VS Code - это нормально!
try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.chrome.options import Options
    # ВАЖНО: убедитесь, что пути к вашим модулям верны внутри контейнера
    from logic.insert_to_db import insert_to_db
    from logic.clean_name import clean_name
    from logic.clean_price import clean_price
except ImportError:
    print("Библиотеки будут доступны внутри Docker!")

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2026, 3, 20),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def run_crypto_scraper_logic():
    """Ваша основная логика скрапинга"""
    print("--- DEBUG INFO START ---")
    print(f"Текущая рабочая директория: {os.getcwd()}")
    
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    print("🌐 Подключаюсь к удаленному Selenium Grid...")
    # Имя хоста 'selenium-chrome' берется из вашего docker-compose.yaml
    driver = webdriver.Remote(
        command_executor='http://selenium-chrome:4444/wd/hub',
        options=options
    )
    
    try:
        print("🚀 Старт скрапера на CoinMarketCap...")
        driver.get("https://coinmarketcap.com/")
        import time
        time.sleep(5) 
        
        rows = driver.find_elements(By.CSS_SELECTOR, "table.cmc-table tbody tr")
        print(f"✅ Найдено строк: {len(rows)}")
        
        for row in rows[:15]:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            try:
                name = row.find_element(By.CSS_SELECTOR, "td:nth-child(3)").text
                name_clean = clean_name(name)
                
                # Селектор цены может быть капризным, добавили проверку
                price_text = row.find_element(By.CSS_SELECTOR, 'div [class*="sc-"] > span').text
                price_clean = clean_price(price_text)
                
                print(f"💾 Сохраняю: {name_clean} - {price_clean}")
                insert_to_db(name_clean, price_clean, current_time)
            except Exception as e:
                print(f"⚠️ Пропуск строки: {e}")
                continue
                
    finally:
        driver.quit()
        print("🏁 Работа завершена, драйвер закрыт.")

# Описываем сам DAG
with DAG(
    'crypto_market_scraper_v1',
    default_args=default_args,
    description='My beautiful crypto scraper',
    schedule_interval=timedelta(hours=4), #schedule_interval=timedelta(days=1),
    catchup=False
) as dag:

    # ИСПРАВЛЕНО: Создаем задачу, которая будет вызывать вашу функцию
    task_run_scraper = PythonOperator(
        task_id='run_crypto_scraper_task',
        python_callable=run_crypto_scraper_logic,
    )