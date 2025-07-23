import streamlit as st
from pymongo import MongoClient
import pandas as pd

# Conexión a MongoDB (el nombre del servicio en docker-compose es "mongodb")
client = MongoClient("mongodb://mongodb:27017/")
db = client["end_to_end_db"]
collection = db["end"]

# Obtener el último documento insertado
last_doc = collection.find_one(sort=[('_id', -1)])

st.title("🛰️ Dashboard de Datos Ingeridos")

if not last_doc:
    st.warning("No hay datos disponibles aún.")
else:
    st.subheader("🌡️ Clima")
    weather = last_doc.get("clean_weather_data", {})
    if weather:
        df_weather = pd.DataFrame(weather)
        st.line_chart(df_weather.set_index("time"))
    else:
        st.write("Datos de clima no disponibles.")

    st.subheader("💱 Tipos de cambio (MXN base)")
    currency = last_doc.get("clean_currency_data", {})
    if currency:
        rates = currency.get("rates", {})
        st.table(pd.DataFrame.from_dict(rates, orient="index", columns=["Valor"]))
    else:
        st.write("Datos de moneda no disponibles.")

    st.subheader("📰 Noticias principales")
    news = last_doc.get("clean_news_data", [])
    if news:
        for article in news:
            st.markdown(f"### [{article['title']}]({article['url']})")
            st.write(f"*{article['source']}* — {article['published_at']}")
            st.write(article["description"])
            st.caption(article["content_preview"])
            st.markdown("---")
    else:
        st.write("Datos de noticias no disponibles.")


    st.subheader("💸 Conversor de Moneda (desde MXN)")
    amount = st.number_input("Cantidad en pesos mexicanos (MXN):", min_value=0.0, value=100.0, step=10.0)

    available_currencies = list(rates.keys()) if rates else []
    selected_currency = st.selectbox("Selecciona la moneda destino:", available_currencies)

    if st.button("Convertir"):
        rate = rates.get(selected_currency)
        if rate:
            converted = amount * rate
            st.success(f"{amount:.2f} MXN = {converted:.2f} {selected_currency}")
        else:
            st.error("Tipo de cambio no disponible para la moneda seleccionada.")

