import sqlite3
import os
from datetime import datetime

def insert_to_db(coin_name, price, current_time):
    print(f'Запускаем тестовую вставку данных в таблицу БД')
    # Определяем ПРЯМОЙ путь к базе относительно текущего файла
    # Это сработает и в Windows, и в Docker одинаково!
    base_dir = os.path.dirname(os.path.abspath(__file__)) 
    db_path = os.path.join(base_dir, 'scraper_data_v1.db')
    
    print(f"DEBUG: Пытаюсь записать в базу по адресу: {db_path}")

    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO scrap (coin_name, price, date_checked)
            VALUES (?, ?, ?)
        ''', (coin_name, price, current_time))
if __name__ == "__main__":
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    insert_to_db('Mycoin', 99999, current_time)
# import sqlite3
# from datetime import datetime
# def insert_to_db(coin_name, price,  current_time):
#     # Используем with для автоматического закрытия соединения
#     with sqlite3.connect('/opt/airflow/src_2/scraper_data_v1.db') as conn:
#         cursor = conn.cursor()
#         # Открываем файл для чтения данных
        

#         # Вставляем данные в таблицу
#         cursor.execute('''
#             INSERT INTO scrap (coin_name, price,  date_checked)
#             VALUES (?, ?, ?)
#         ''', (coin_name, price, current_time))
        
# current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
# insert_to_db('Mycoin', 99999, current_time)