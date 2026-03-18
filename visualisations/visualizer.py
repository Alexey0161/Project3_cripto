import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np

def show_analytics():
    with sqlite3.connect('books_data_v3.db') as conn:
        # Читаем данные прямо в таблицу Pandas
        df = pd.read_sql_query("SELECT title, avg(price), date_checked FROM books group by title,  date_checked", conn)
        # df = pd.read_sql_query("SELECT * FROM books where title='Tipping the Velvet'", conn)
    # print("Вот как выглядят наши данные в Pandas:")
    # print(df.head()) # Покажет первые 5 строк
    df = df.head(15)
    return df
df = show_analytics()
# print(df, 14)
#     # Тут начнется магия графиков...
# Гистаграмма распределения количества продаж по названиям книг
# def show_bar_chart(df):
#     books = df
    
#     plt.figure(figsize=(10, 6)) # Размер окна (ширина, высота)
#     plt.bar(books['title'], books['sales_volume'], color='skyblue')
    
#     plt.title('Продажи книг за весь период продаж')
#     plt.xlabel('Название книги')
#     plt.ylabel('Количество продаж')
#     plt.xticks(rotation=45, ha='right') # Поворачиваем названия, чтобы они не налезали друг на друга
#     plt.tight_layout() # Автоматически подправляет поля
#     plt.show()

# show_bar_chart(df)

# def show_scatter(df):
#     plt.figure(figsize=(8, 5))
#     plt.scatter(df['price'], df['stock_count'], color='salmon', alpha=0.6)
    
#     plt.title('Зависимость остатков на складе от цены')
#     plt.xlabel('Цена (£)')
#     plt.ylabel('Остаток на складе')
#     plt.grid(True, linestyle='--', alpha=0.7) # Добавляем сеточку
#     plt.show()

# show_scatter(df)

# def show_dinamic(df):
#     print(df, 48)
#     # ваши данные
#     # x = [1, 2, 3, 4, 5]
#     time_checked = df['date_checked']
#     # print(type(x), 54)
#     x = []
#     for i in time_checked :
#         ind = i.find(' ')
#         # print(i, ind, 54)
        
#         i = i[ind+1 :]
#         x.append(i)
#     # print(x, 60)
#     # y = [2, 3, 5, 7, 11]
#     y = df['avg(price)'].values
#     # avg = np.mean(y)
#     print(y,df['avg(price)'],  64)

#     # построение графика
#     plt.plot(x, y)
#     plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')

#     # добавление заголовка и подписей
#     plt.title("Линейная динамика изменения цены первых трех книг списка")
#     plt.xlabel("Ось date_checked")
#     plt.ylabel("Ось price")
#     plt.show()




def show_dinamic(df):
    plt.figure(figsize=(10, 6))
    
    # 1. Получаем список уникальных книг в нашем наборе
    unique_books = df['title'].unique()
    
    # 2. Рисуем линию ДЛЯ КАЖДОЙ книги отдельно
    for book in unique_books:
        # Фильтруем данные только для текущей книги
        book_data = df[df['title'] == book]
        
        # Обрезаем время (ваш удачный маневр!)
        times = [t.split(' ')[1] for t in book_data['date_checked']]
        prices = book_data['avg(price)']
        
        # Рисуем линию этой книги и даем ей имя для легенды
        plt.plot(times, prices, marker='o', label=book)

    plt.title("Динамика цен: Сравнение книг")
    plt.xlabel("Время замера")
    plt.ylabel("Цена (£)")
    plt.legend() # Добавляет подписи (какой цвет какая книга)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.show()
# отображение графика
show_dinamic(df)