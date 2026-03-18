import sqlite3
from datetime import datetime
def insert_to_db(coin_name, price,  current_time):
    # Используем with для автоматического закрытия соединения
    with sqlite3.connect('scraper_data_v1.db') as conn:
        cursor = conn.cursor()
        # Открываем файл для чтения данных
        

        # Вставляем данные в таблицу
        cursor.execute('''
            INSERT INTO scrap (coin_name, price,  date_checked)
            VALUES (?, ?, ?)
        ''', (coin_name, price, current_time))
        
# current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
# insert_to_db('Mycoin', 99999, current_time)