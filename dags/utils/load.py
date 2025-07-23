from pymongo import MongoClient, errors

def load(ti):
    complete_data = ti.xcom_pull(key="complete_data", task_ids="transform_task")
    if not complete_data:
        print("No hay datos para cargar")
        return
    try:
        client = MongoClient("mongodb://mongodb:27017/")
        db = client["end_to_end_db"]
        collection = db["end"]
        result = collection.insert_one(complete_data)
        print(f'Datos insertados con id: {result.inserted_id}')
    except errors.PyMongoError as e:
        print(f'Error al insertar en MongoDB: {e}')