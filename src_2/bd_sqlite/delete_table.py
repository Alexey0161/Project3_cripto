import sqlite3

with sqlite3.connect('scraper_data_v1.db') as conn:
    cursor = conn.cursor()
    # Очистить таблицу, удалив все записи
    cursor.execute('DELETE FROM scrap')