from fastapi import FastAPI

# Создаем экземпляр приложения
app = FastAPI(
    title="Crypto Analytics API",
    description="Интерфейс для работы с данными скрапера криптовалют",
    version="1.0.0",
)


@app.get("/")
def home():
    return {
        "message": "Выполнен вход в API",
        "instruction": "Перейдите на /docs для просмотра документации",
    }


@app.get("/health")
def health_check():
    return {"status": "alive", "db_connected": "waiting for connection"}
