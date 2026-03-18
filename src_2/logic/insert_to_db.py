import sqlite3
def save_to_db(title, price, sales, stock, current_time):
    # Используем with для автоматического закрытия соединения
    with sqlite3.connect('books_data_v3.db') as conn:
        cursor = conn.cursor()
        # Открываем файл для чтения данных
        

        # Вставляем данные в таблицу
        cursor.execute('''
            INSERT INTO books (coin_name, price,  date_checked)
            VALUES (?, ?, ?)
        ''', (title, price, sales, stock, current_time))