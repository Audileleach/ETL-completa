import requests

def currency_extraction(ti): #Función para extraer datos
#{'latitude': 21.0, 'longitude': -89.625, 'generationtime_ms': 0.02384185791015625, 'utc_offset_seconds': -21600, 'timezone': 'America/Merida', 'timezone_abbreviation': 'GMT-6', 'elevation': 11.0, 'hourly_units': {'time': 'iso8601', 'temperature_2m': '°C'}
# hourly
# temperature_2m
    url = "https://api.fxratesapi.com/latest?base=MXN&symbols=USD,EUR,JPY,GBP,CNY&api_key=fxr_live_d7fe163296919cf6a6ad6fca3198d54849a9" #URL de la API

    response = requests.get(url) #Hace una solicitud GET a la URL

    if response.status_code == 200: #Checa que la respuesta sea exitosa
        data = response.json() #Convierte el contenido JSON a un diccionario de Python
        ti.xcom_push(key="extracted_currency_api_data", value=data)
    else: #en cualquier otro caso retorna un diccionario con un mensaje de error
        data = {"error": "Failed to fetch data, status code: " + str(response.status_code)}
        ti.xcom_push(key="extracted_currency_api_data", value=data)