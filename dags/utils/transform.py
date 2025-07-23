from datetime import datetime

def transform(ti):
    weather_data = ti.xcom_pull(key="extracted_weather_api_data", task_ids="extract_weather_api_task")
    currency_data = ti.xcom_pull(key="extracted_currency_api_data", task_ids="extract_currency_api_task")
    news_data = ti.xcom_pull(key="extracted_news_api_data", task_ids="extract_news_api_task")

    raw_times = weather_data["hourly"]["time"]
    raw_temperatures = weather_data["hourly"]["temperature_2m"]

    processed_times = [datetime.fromisoformat(t).strftime("%Y-%m-%d %H:%M") for t in raw_times]

    clean_weather_data = {"time": processed_times, "temperature_2m": raw_temperatures}
    clean_currency_data = {"base": currency_data["base"], "rates": currency_data["rates"]}
    clean_news_data = [
        {
            "source": article.get("source", {}).get("name", ""),
            "author": article.get("author", ""),
            "title": article.get("title", ""),
            "description": article.get("description", ""),
            "url": article.get("url", ""),
            "published_at": article.get("publishedAt", ""),
            "content_preview": article.get("content", "")[:100] if article.get("content") else ""
        }
        for article in news_data.get("articles", []) if isinstance(article, dict)
    ]

    ti.xcom_push(key="complete_data", value={
        "clean_weather_data": clean_weather_data,
        "clean_currency_data": clean_currency_data,
        "clean_news_data": clean_news_data
    })
