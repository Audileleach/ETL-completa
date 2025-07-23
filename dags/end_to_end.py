from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import pymongo
from pymongo import MongoClient, errors
import requests

from utils.weather_extraction import weather_extraction
from utils.currency_extraction import currency_extraction
from utils.news_extraction import news_extraction
from utils.transform import transform
from utils.load import load



dag = DAG(
    'end_to_end',
    description='This ingestion DAG populates mongodb',
    start_date=datetime(2025, 7, 15),
    schedule_interval='@daily',
    catchup=False
)

extract_weather_api_task = PythonOperator(
    task_id = "extract_weather_api_task",
    python_callable=weather_extraction,
    dag=dag
)

extract_currency_api_task = PythonOperator(
    task_id = "extract_currency_api_task",
    python_callable=currency_extraction,
    dag=dag
)

extract_news_api_task = PythonOperator(
    task_id = "extract_news_api_task",
    python_callable=news_extraction,
    dag=dag
)

transform_task = PythonOperator(
    task_id = "transform_task",
    python_callable=transform,
    dag=dag
)

load_task = PythonOperator(
    task_id="load_task",
    python_callable=load,
    dag=dag
)

extract_weather_api_task >> transform_task
extract_currency_api_task >> transform_task
extract_news_api_task >> transform_task
transform_task >> load_task