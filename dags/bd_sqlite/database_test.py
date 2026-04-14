######## Работающий код ##############
# import sqlite3

# connection = sqlite3.connect(
#     "C:/Users/ivano/Desktop/Project3_CryptoScraper/dags/logic/scraper_data_v1.db"
# )
# cursor = connection.cursor()
##############################################

# cursor.execute("""
# CREATE TABLE IF NOT EXISTS scrap (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     coin_name TEXT,
#     coin_ticker TEXT,
#     price REAL,           -- Цена (число)
#     date_checked TIMESTAMP -- Время замера
# )
# """)


def ensure_db_exists():
    import sqlite3
    import os
    path = os.path.dirname(__file__)
    parent_path = os.path.dirname(path)
    print(parent_path, 24)  # Вывод: dags

    
    # Путь к папке dags/bd_sqlite (относительно текущего файла)
    db_dir = os.path.join(parent_path, 'logic')
    os.makedirs(db_dir, exist_ok=True) # Создаем папку, если её нет
    
    db_path = os.path.join(db_dir, 'scraper_data_v1.db')
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS scrap (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        coin_name TEXT,
        coin_ticker TEXT,
        price REAL,           -- Цена (число)
        date_checked TIMESTAMP -- Время замера
    )
    ''')
    conn.commit()
    conn.close()
