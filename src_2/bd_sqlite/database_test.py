import sqlite3
from datetime import datetime # Импортируем время


connection = sqlite3.connect("scraper_data_v1.db")
cursor = connection.cursor()


cursor.execute('''
CREATE TABLE IF NOT EXISTS scrap (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    coin_name TEXT,
    price REAL,           -- Цена (число)
    date_checked TIMESTAMP -- Время замера
)
''')