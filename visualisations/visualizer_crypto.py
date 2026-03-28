import sqlite3
import matplotlib.pyplot as plt
import pandas as pd
import os

def get_crypto_data():
    # 1. Путь к базе! 
    
    db_path = "C:/Users/ivano/Desktop/Project3_CryptoScraper/dags/logic/scraper_data_v1.db"
    if not os.path.exists(db_path):
        print(f" Ошибка: Файл базы данных не найден по пути: {db_path}")
        return None

    try:
        with sqlite3.connect(db_path) as conn:
            
            query = """
            SELECT coin_name, coin_ticker, price, date_checked
            FROM scrap
            ORDER BY date_checked ASC
            """
            df = pd.read_sql_query(query, conn)
            return df
    except Exception as e:
        print(f"Ошибка при чтении БД: {e}")
        return None

def create_artifacts(df):
    if df is None or df.empty:
        print(" Данных для анализа нет.")
        return

    # 1. Превращаем текст в объекты даты/времени (Магия Pandas)
    df['date_checked'] = pd.to_datetime(df['date_checked'])
    df = df.sort_values('date_checked') # Сортируем, чтобы линии не прыгали назад

    # 2. Создаем полотно побольше
    plt.figure(figsize=(15, 8)) 
    
    # Берем ТОП-3 монеты (например, Bitcoin, Ethereum и еще одну)
    top_coins = df["coin_name"].unique()[:3] 

    for coin in top_coins:
        coin_data = df[df["coin_name"] == coin]
        
        # Используем полную колонку даты для оси X
        plt.plot(coin_data["date_checked"], coin_data["price"], 
                 marker="o", markersize=4, label=coin, linewidth=2)

    # 3. Настройка осей и масштаба
    plt.yscale('log') # Логарифмическая шкала: теперь $70k и $2k на одном графике
    
    # Ограничиваем количество подписей на оси X, чтобы не было "черной полосы"
    plt.gca().xaxis.set_major_locator(plt.MaxNLocator(10)) 
    
    # Красивое оформление
    plt.title("Динамика цен криптовалют (Проект 3: Артефакт №1)", fontsize=16, fontweight='bold')
    plt.xlabel("Дата и время замера", fontsize=12)
    plt.ylabel("Цена (USD) - Логарифмическая шкала", fontsize=12)
    
    plt.xticks(rotation=30) # Поворачиваем даты
    plt.legend(title="Криптовалюты", fontsize=10)
    plt.grid(True, which="both", linestyle="--", alpha=0.5)
    plt.tight_layout()
    
    # Сохраняем результат
    plt.savefig("crypto_chart_clean.png")
    print("график сохранен: crypto_chart_clean.png")

    # --- АРТЕФАКТ 2: Сводный отчет в CSV ---
    report = df.groupby("coin_name")["price"].agg(["mean", "min", "max", "count"]).reset_index()
    report.columns = ["Валюта", "Средняя цена", "Минимум", "Максимум", "Кол-во замеров"]
    report.to_csv("crypto_report.csv", index=False, encoding="utf-8-sig")
    print("Сводный отчет сохранен: crypto_report.csv")
    
    plt.show()
    # --- АРТЕФАКТ 2: Сводная таблица (CSV) ---
    # Группируем и считаем среднее, мин и макс
    report = df.groupby("coin_name")["price"].agg(["mean", "min", "max"]).reset_index()
    report.columns = ["Валюта", "Средняя цена", "Минимум", "Максимум"]
    
    report.to_csv("crypto_report.csv", index=False, encoding="utf-8-sig")
    print(" Отчет сохранен: crypto_report.csv")
    
    plt.show()

# Запуск процесса
if __name__ == "__main__":
    data = get_crypto_data()
    create_artifacts(data)