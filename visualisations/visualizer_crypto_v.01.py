import sqlite3
import matplotlib.pyplot as plt
import pandas as pd
import os

def get_crypto_data():
    
        # Получаем директорию, где находится текущий скрипт
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(script_dir)
    
    # Строим путь к БД относительно этой директории
    db_path = os.path.join(parent_dir, 'dags', 'logic', 'scraper_data_v1.db')
    
    
    if not os.path.exists(db_path):
        print("Ошибка: Файл базы данных не найден!")
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
        print(f" Ошибка при чтении БД: {e}")
        return None

def create_artifacts(df):
    if df is None or df.empty:
        print("Данных для анализа нет.")
        return

    # --- 1. ОЧИСТКА ДАННЫХ  ---
    # Убираем  ошибки скрапинга: BTC не может стоить меньше 10k в 2026 году
    df = df.drop(df[(df['coin_name'] == 'Bitcoin') & (df['price'] < 10000)].index)
    # Убираем пустые или маленькие цены (чтобы они мешают логарифмической шкале)
    df = df[df['price'] > 1] 

    # --- 2. ПОДГОТОВКА ШКАЛЫ ВРЕМЕНИ ---
    df['date_checked'] = pd.to_datetime(df['date_checked'])
    # Сортируем сначала по имени, потом по дате для правильных линий
    df = df.sort_values(by=['coin_name', 'date_checked']) 

    # --- 3. ГРАФИК (Артефакт №1) ---
    plt.figure(figsize=(15, 8)) 
    
    top_coins = df["coin_name"].unique()[:3] 

    for coin in top_coins:
        coin_data = df[df["coin_name"] == coin]
        
        plt.plot(coin_data["date_checked"], coin_data["price"], 
                 marker="o", markersize=2, label=coin, linewidth=1.5)

    plt.yscale('log') 
    plt.gca().xaxis.set_major_locator(plt.MaxNLocator(10)) 
    
    plt.title("Динамика цен криптовалют (Очищенные данные)", fontsize=16, fontweight='bold')
    plt.xlabel("Дата и время замера", fontsize=12)
    plt.ylabel("Цена (USD) - Log scale", fontsize=12)
    
    plt.xticks(rotation=30)
    plt.legend(title="Криптовалюты", loc='upper left')
    plt.grid(True, which="both", linestyle="--", alpha=0.3)
    plt.tight_layout()
    
    plt.savefig("crypto_chart_final.png")
    print("График сохранен: crypto_chart_final.png")

# --- АРТЕФАКТ №4: Индивидуальные графики  ---
    fig,axes = plt.subplots(len(top_coins), 1, figsize=(15, 12), sharex=True)
    
    for i, coin in enumerate(top_coins):
        coin_data = df[df["coin_name"] == coin]
        axes[i].plot(coin_data["date_checked"], coin_data["price"], 
                     color=f'C{i}', label=f"Динамика {coin}")
        
        # не используем логарифм, чтобы  график захватил центы этой монеты
        axes[i].set_ylabel("Цена (USD)")
        axes[i].legend(loc='upper left')
        axes[i].grid(True, alpha=0.3)

    plt.xlabel("Дата и время")
    plt.suptitle("Детальный анализ волатильности (Micro-scale)", fontsize=16)
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.savefig("crypto_micro_dynamics.png")
    print("Дополнительный артефакт сохранен: crypto_micro_dynamics.png")

    # --- 5. СВОДНЫЙ ОТЧЕТ (Артефакт №2) ---
    report1 = (df.groupby("coin_name")["price"].agg("max") -
           df.groupby("coin_name")["price"].agg("min")) / \
          df.groupby("coin_name")["price"].agg("count") * 2

    # Шаг 5.1: Преобразуем report1 в DataFrame и переименовываем колонки
    temp_change = report1.reset_index()
    temp_change.columns = ['Валюта', 'Темп изменения цены']

    # Шаг 5.2: создаём основной отчёт
    report = df.groupby("coin_name")["price"].agg(
        ["mean", "min", "max", "count"]
    ).reset_index()

    # Переименовываем колонки в report
    report.columns = ["Валюта", "Средняя цена", "Минимум", "Максимум", "Кол-во замеров"]

    # Шаг 5.3: объединяем таблицы
    final_report = pd.merge(report, temp_change, on='Валюта', how='left')

    # Шаг 5.4: Выводим результат
    print(final_report)
    final_report.to_csv("crypto_report_final.csv", index=False, encoding="utf-8-sig")
    print("Сводный отчет сохранен: crypto_report_final.csv")
    
    plt.show()

if __name__ == "__main__":
    data = get_crypto_data()
    create_artifacts(data)