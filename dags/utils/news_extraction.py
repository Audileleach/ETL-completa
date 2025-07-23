import requests

def news_extraction(ti): #Función para extraer datos

    url = "https://newsapi.org/v2/top-headlines?country=us&apiKey=c491f602c3224dccbe769e8a07708387&pageSize=5" #URL de la API

    response = requests.get(url) #Hace una solicitud GET a la URL

    if response.status_code == 200: #Checa que la respuesta sea exitosa
        data = response.json() #Convierte el contenido JSON a un diccionario de Python
        ti.xcom_push(key="extracted_news_api_data", value=data)
    else: #en cualquier otro caso retorna un diccionario con un mensaje de error
        data = {"error": "Failed to fetch data, status code: " + str(response.status_code)}
        ti.xcom_push(key="extracted_news_api_data", value=data)