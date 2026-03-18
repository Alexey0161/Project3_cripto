import sqlite3

with sqlite3.connect('books_data_v3.db') as conn:
    cursor = conn.cursor()
    # Очистить таблицу, удалив все записи
    cursor.execute('DELETE FROM books')