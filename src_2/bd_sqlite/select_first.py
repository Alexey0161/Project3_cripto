import sqlite3

conn = sqlite3.connect("scraper_data_v1.db")
conn = sqlite3.connect("C:/Users/ivano/Desktop/Project3_CryptoScraper/dags/logic/scraper_data_v1.db")
# conn = sqlite3.connect("C:/Users/ivano/Desktop/Project3_CryptoScraper/src_2/logic/scraper_data_v1.db")

cursor = conn.cursor()

##1 SQL-запрос (выбрать все записи)
query = "SELECT coin_name, price, date_checked FROM scrap"

cursor.execute(query)

results = cursor.fetchall()

# Обработка результатов
for result in results:
    print(result)

conn.close()
