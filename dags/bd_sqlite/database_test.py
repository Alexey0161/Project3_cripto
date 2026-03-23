import sqlite3

connection = sqlite3.connect(
    "C:/Users/ivano/Desktop/Project3_CryptoScraper/dags/logic/scraper_data_v1.db"
)
cursor = connection.cursor()


cursor.execute("""
CREATE TABLE IF NOT EXISTS scrap (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    coin_name TEXT,
    coin_ticker TEXT,
    price REAL,           -- Цена (число)
    date_checked TIMESTAMP -- Время замера
)
""")
