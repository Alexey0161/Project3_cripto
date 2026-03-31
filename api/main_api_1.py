import sqlite3
import os
from fastapi import FastAPI, Query # по всей видимости в инструменте fastapi есть нечто наподобие запроса sql?
from typing import Optional # вообще не понимаю что это  и для чего мы этот инструмент берем в код?
from pydantic import BaseModel
from typing import List


# Схема для ОДНОЙ записи о монете (соответствует колонкам в БД)
class CryptoCoin(BaseModel):
    id: int
    coin_name: str
    coin_ticker: str
    price: float
    date_checked: str

# Схема для всего ОТВЕТА (то, что видит пользователь)
class APIResponse(BaseModel):
    count: int
    version: str
    result: List[CryptoCoin]

app = FastAPI(title="Crypto Analytics API", version="1.1.0") #  вот это значение - version="1.1.0"  мы установили произвольно

# Путь к твоей базе (учитывая структуру проекта)
script_dir = os.path.dirname(__file__)
# print(os.path.dirname(script_dir), 10)
parents_dir = os.path.dirname(script_dir)
DB_PATH = os.path.join(parents_dir, "dags", "logic", "scraper_data_v1.db")

def get_db_data(ticker: str = None, limit: int = 10, offset: int = 0): # это некая функция с аннотацией типов и заданием значений
    """Функция для извлечения данных с фильтром и пагинацией (для экономии трафика)"""
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row  #  это что? --- стандартный синтаксис, чтобы перевести строку таблицы БД в словарь?
        # что такое conn.row_factory? Дальше в коде мы это не используем?
        
        cursor = conn.cursor() #  что такое метод  cursor()? Какие у него возможности, что он делает?
        
        query = "SELECT * FROM scrap"  # здесь мы пишем базовый запрос sql  к таблице?
        params = []  # создаем список? Для чего?
        
        if ticker: #  чтобы код не падал по ошибке, отсекаем варианты когда тикера в БД по каким-либо причинам нет
            query += " WHERE coin_ticker = ?" # в синтаксисе sql по сути это фильтрация данных? Так как query - это строка
            # то к ней можно через "+" добавлять еще символы или целые строки. Но что значит знак "?". По идее sql запрос так 
            # работать не может
            
            params.append(ticker.upper()) # к списку добавляем значение в верхнем регистре переменной ticker, которое мы 
            # получаем из таблицы БД, таким образом мы получаем список тикеров из запроса query
            
        query += " ORDER BY date_checked DESC LIMIT ? OFFSET ?" # сортируем выборку из запроса убыванию даты берем LIMIT
        # по умолчанию 10 валют, а что за параметр OFFSET?
        params.extend([limit, offset]) # здесь мы добавляем список значений переменных  limit, offset 
        # заданных по умолчанию в конец списка?
        
        cursor.execute(query, params) # Что это за синтаксис? Какие параметры может принимать функция execute()?
        # и в данном случае похоже, что cursor - это вся  таблица БД?
        return [dict(row) for row in cursor.fetchall()]
        
# @app.get("/prices", tags=["Данные"]) # судя по синтаксису - это декоратор. Но какой? Какой-то стандартный, который похоже, что формирует графику 
# # на странице браузера
# def read_prices(
#     ticker: Optional[str] = Query(None, description="Тикер монеты (напр. BTC)"),
#     limit: int = Query(10, le=100, description="Сколько записей вернуть"),
#     offset: int = Query(0, description="Сколько записей пропустить")
# ):
#     """
#     Получение среза данных. Реализована фильтрация по тикеру 
#     и ограничение объема (пагинация) для защиты трафика.
#     """
#     data = get_db_data(ticker, limit, offset)
#     # return {"count": len(data), "result": data}
#     return {"count": len(data), "version": "1.1.0", "result": data}


@app.get(
    "/prices", 
    tags=["Данные"], 
    response_model=APIResponse, # <--- ЭТО САМОЕ ГЛАВНОЕ!
    summary="Получить актуальные цены криптовалют"
)
def read_prices(
    ticker: Optional[str] = Query(None, description="Тикер монеты (напр. BTC)"),
    limit: int = Query(10, le=100, description="Сколько записей вернуть (макс 100)"),
    offset: int = Query(0, description="Сколько записей пропустить")
):
    """
    Эндпоинт возвращает срез данных из БД.
    Реализована пагинация (limit/offset) и фильтрация по тикеру.
    """
    data = get_db_data(ticker, limit, offset)
    # Возвращаем словарь, который FastAPI проверит по схеме APIResponse
    return {
        "count": len(data), 
        "version": "1.1.0", 
        "result": data
    }