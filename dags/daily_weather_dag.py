# daily_weather_dag.py
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from weather_fetcher import fetch_weather_data
from db_writer import insert_weather_data


CITY = "Hyderabad"
API_KEY = "7320f0f7496906e5a4de5f728339c420"

def fetch_and_store():
    data = fetch_weather_data(CITY, API_KEY)
    insert_weather_data(data)

default_args = {
    "owner": "airflow",
    "retries": 1,
    "retry_delay": timedelta(minutes=5)
}

with DAG(
    dag_id="daily_weather_report",
    default_args=default_args,
    description="Fetch and store daily weather data",
    start_date=datetime(2025, 5, 1),
    schedule_interval="0 */4 * * *",  
    catchup=True,
) as dag:

    fetch_store_task = PythonOperator(
        task_id="fetch_and_store_weather",
        python_callable=fetch_and_store
    )

