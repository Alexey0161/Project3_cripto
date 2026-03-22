from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys
import os

# 1. Добавляем путь к папке src_2 в системе Docker
sys.path.append('/opt/airflow/src_2')

# 2. ПРЯМОЙ ИМПОРТ (без try-except, чтобы видеть реальную ошибку, если она есть)
from scraper.scraper_cripto import run_crypto_scraper

default_args = {
    'owner': 'Alexey',
    'start_date': datetime(2026, 3, 19),
    'retries': 1,
    'retry_delay': timedelta(minutes=5), 
}

with DAG(
    'crypto_market_scraper_v1',
    default_args=default_args,
    schedule_interval='@hourly',
    catchup=False
) as dag:

    task_run = PythonOperator(
        task_id='fetch_crypto_data',
        python_callable=run_crypto_scraper # Теперь он ТОЧНО должен её увидеть
    )