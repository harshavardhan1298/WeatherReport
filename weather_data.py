# weather_fetcher.py
import requests
from datetime import datetime

def fetch_weather_data(city: str, api_key: str):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    data = response.json()

    if data["cod"] != 200:
        raise Exception(data.get("message", "Error fetching data"))

    return {
        "city": city,
        "temperature": data["main"]["temp"],
        "humidity": data["main"]["humidity"],
        "pressure": data["main"]["pressure"],
        "wind_speed": data["wind"]["speed"],
        "description": data["weather"][0]["description"],
        "datetime": datetime.now()
    }
