import sqlite3
import os
from fastapi import (
    FastAPI,
    Query,
)  
from typing import (
    Optional,
)  
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


app = FastAPI(
    title="Crypto Analytics API", version="1.1.0"
) 

# Путь к  базе (учитывая структуру проекта)
script_dir = os.path.dirname(__file__)

parents_dir = os.path.dirname(script_dir)
DB_PATH = os.path.join(parents_dir, "dags", "logic", "scraper_data_v1.db")


def get_db_data(
    ticker: str = None, limit: int = 10, offset: int = 0
):  
    """Функция для извлечения данных с фильтром и пагинацией (для экономии трафика)"""
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row  
        cursor = (
            conn.cursor()
        )  
        query = "SELECT * FROM scrap"  # здесь мы пишем базовый запрос sql  к таблице
        params = []  

        if ticker:  #  чтобы код не падал по ошибке, отсекаем варианты когда тикера в БД по каким-либо причинам нет
            query += " WHERE coin_ticker = ?"  #  фильтрация данных по тикеру
            params.append(
                ticker.upper()
            )  
            # таким образом мы получаем список тикеров из запроса query

        query += " ORDER BY date_checked DESC LIMIT ? OFFSET ?"  # сортируем выборку из запроса убыванию даты берем LIMIT
        # по умолчанию 10 валют
        params.extend(
            [limit, offset]
        )  

        cursor.execute(
            query, params
        )  
        return [dict(row) for row in cursor.fetchall()]



@app.get(
    "/prices",
    tags=["Данные"],
    response_model=APIResponse,  
    summary="Получить актуальные цены криптовалют",
)
def read_prices(
    ticker: Optional[str] = Query(None, description="Тикер монеты (напр. BTC)"),
    limit: int = Query(10, le=15, description="Сколько записей вернуть (макс 15)"),
    offset: int = Query(0, description="Сколько записей пропустить"),
):
    """
    Эндпоинт возвращает срез данных из БД.
    Реализована пагинация (limit/offset) и фильтрация по тикеру.
    """
    data = get_db_data(ticker, limit, offset)
    # Возвращаем словарь, который FastAPI проверит по схеме APIResponse
    return {"count": len(data), "version": "1.1.0", "result": data}
