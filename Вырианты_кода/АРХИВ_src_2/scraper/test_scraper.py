import sys
import sqlite3
from selenium import webdriver
from selenium.webdriver.common.by import By # Помогает искать элементы
import time
from datetime import datetime # Импортируем время
import random
# from src_1.scraper.database_test import save_to_db
driver = webdriver.Chrome()


def save_to_db(title, price, sales, stock, current_time):
    # Используем with для автоматического закрытия соединения
    with sqlite3.connect('books_data_v3.db') as conn:
        cursor = conn.cursor()
        # Открываем файл для чтения данных
        

        # Вставляем данные в таблицу
        cursor.execute('''
            INSERT INTO books (title, price,  sales_volume, stock_count, date_checked)
            VALUES (?, ?, ?, ?, ?)
        ''', (title, price, sales, stock, current_time))
# База данных автоматически закроется после выхода из блока with

try:
    # 1. Заходим на сайт
    driver.get("http://books.toscrape.com/")
    time.sleep(2) # Дадим странице прогрузиться

    # 2. Ищем заголовок первой книги
    # Мы ищем тег <h3>, внутри которого лежит ссылка <a> с названием
    book_title = driver.find_elements(By.TAG_NAME, "h3")#.find_elements(By.TAG_NAME, "a")#.get_attribute("title")
    # 3. Ищем цену
    # Мы ищем элемент с классом 'price_color'
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    book_price = driver.find_elements(By.CLASS_NAME, "price_color")#.text

    # for j in zip(book_title, book_price):
    #     title = j[0].find_element(By.TAG_NAME, "a").get_attribute("title")
    #     raw_price = j[1].text # Получаем строку вроде "£51.77"
        
    #     # Очищаем цену: убираем символ валюты и превращаем в число
    #     # replace('£', '') уберет значок, float() сделает числом
    #     clean_price = float(raw_price.replace('£', '').replace('Â', '')) 
        
    #     print(f'Название книги: {title} Цена: {clean_price}')
    #     save_to_db(title, clean_price, current_time)
    # Внутри цикла:
    for j in zip(book_title, book_price):
        title = j[0].find_element(By.TAG_NAME, "a").get_attribute("title")
        # 1. Чистим цену
        price = float(j[1].text.replace('£', '').replace('Â', ''))
        # 1.1. Имитируем изменение цены
        price = price - random.randint(0, 10)
        # 2. Имитируем бизнес-процесс
        sales = random.randint(0, 8)  # Сколько купили сегодня
        
        # Для простоты: пусть склад каждый раз генерируется как 50 - sales, 
        # чтобы мы видели, как он меняется.
        stock = 50 - random.randint(sales, 40) 
    
        # 3. Сохраняем (не забудьте обновить аргументы функции!)
        save_to_db(title, price, sales, stock, current_time)        
finally:
    driver.quit()