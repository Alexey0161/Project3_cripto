import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "libs"))
from datetime import datetime, timedelta  # ИСПРАВЛЕНО: добавили timedelta

# Настраиваем пути, чтобы видеть папку logic
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)
# Пытаемся импортировать Airflow (сработает только в контейнере)
try:
    from airflow import DAG
    from airflow.operators.python import PythonOperator

    AIRFLOW_AVAILABLE = True
except ImportError:
    AIRFLOW_AVAILABLE = False
    print("⚠️ Airflow не найден. Работаю в режиме прямого запуска.")
# Определяем путь к папке dags
dags_folder = os.path.dirname(__file__)

# Добавляем путь к библиотекам libs
libs_path = os.path.join(dags_folder, "libs")
if libs_path not in sys.path:
    sys.path.insert(0, libs_path)

# Добавляем путь к папке logic (она лежит в dags )
if dags_folder not in sys.path:
    sys.path.insert(0, dags_folder)
# Эти импорты могут подчеркиваться желтым в VS Code - это нормально!
try:
    from logic.clean_name import clean_name
    from logic.clean_price import clean_price
    from logic.clean_ticker import clean_ticker
    from bd_sqlite.database_test import ensure_db_exists
    # ВАЖНО: убедиться, что пути к  модулям верны внутри контейнера
    from logic.insert_to_db import insert_to_db
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
except ImportError:
    print("Библиотеки будут доступны внутри Docker!")

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2026, 3, 20),
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

ensure_db_exists()
def run_crypto_scraper_logic():
    """Ваша основная логика скрапинга"""
    print("--- DEBUG INFO START ---")
    print(f"Текущая рабочая директория: {os.getcwd()}")

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    print("🌐 Подключаюсь к удаленному Selenium Grid...")
    # Определяем, где мы находимся
    # В Docker-контейнере  есть специфические переменные окружения
    IS_DOCKER = os.path.exists("/.dockerenv")

    if IS_DOCKER:
        # Адрес для работы внутри сети Docker
        selenium_url = "http://selenium-chrome:4444/wd/hub"
    else:
        # Адрес для работы из Windows (обращаемся к опубликованному порту)
        selenium_url = "http://localhost:4444/wd/hub"

    print(f"🌐 Подключаюсь к Selenium по адресу: {selenium_url}")
    # Имя хоста 'selenium-chrome' берется из  docker-compose.yaml
    driver = webdriver.Remote(
        command_executor=selenium_url,  # Используем нашу умную переменную! command_executor='http://selenium-chrome:4444/wd/hub',
        options=options,
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

                # добавляю блок извлечения тикера:
                ticker = clean_ticker(name)

                # Селектор цены может быть капризным, поэтому добавляю проверку
                price_text = row.find_element(
                    By.CSS_SELECTOR, 'div [class*="sc-"] > span'
                ).text
                price_clean = clean_price(price_text)

                print(
                    f"💾 Сохраняю: {name_clean} - {ticker} - {price_clean}", 208
                )  # - {ticker}
                insert_to_db(name_clean, ticker, price_clean, current_time)
            except Exception as e:
                print(f"⚠️ Пропуск строки: {e}")
                continue

    finally:
        driver.quit()
        print("🏁 Работа завершена, драйвер закрыт.")


if AIRFLOW_AVAILABLE:
    # Описываем сам DAG
    with (
        DAG(
            "crypto_market_scraper_v1",
            default_args=default_args,
            description="My beautiful crypto scraper",
            schedule_interval=timedelta(minutes=2),  # Ставим 10 минут! 🚀schedule_interval=timedelta(hours=4), #schedule_interval=timedelta(days=1),
            catchup=False
        ) 
    ):
        # ИСПРАВЛЕНО: Создаем задачу, которая будет вызывать  функцию
        task_run_scraper = PythonOperator(
            task_id="run_crypto_scraper_task",
            python_callable=run_crypto_scraper_logic,
        )
else:
    # Если мы не в Airflow, просто запускаем функцию при старте файла
    if __name__ == "__main__":
        from datetime import datetime

        print("🚀 Запуск скрапера вручную...")
        # Вызываем вашу основную функцию (как она  называется в Даге)
        run_crypto_scraper_logic()
