from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from pymongo import MongoClient, errors

def read_from_mongo():
    try:
        client = MongoClient("mongodb://mongodb:27017/")  # Conexión interna dentro de Docker
        db = client["end_to_end_db"]
        collection = db["end"]

        documents = list(collection.find().limit(5))  # Solo los primeros 5 documentos
        if documents:
            print("📄 Documentos encontrados:")
            for doc in documents:
                print(doc)
        else:
            print("⚠️ No se encontraron documentos en la colección.")
    except errors.PyMongoError as e:
        print(f"❌ Error al leer desde MongoDB: {e}")

default_args = {
    'start_date': datetime(2025, 7, 22),
    'catchup': False
}

with DAG(
    'read_from_mongo_dag',
    description='Lee datos desde MongoDB y los muestra en los logs de Airflow',
    schedule_interval=None,
    default_args=default_args,
    tags=['debug', 'mongo']
) as dag:

    read_task = PythonOperator(
        task_id='read_mongo_data_task',
        python_callable=read_from_mongo
    )
