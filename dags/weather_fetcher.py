import requests
import json
from datetime import datetime

def fetch_weather_data(city, api_key):
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric"  
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  

        data = response.json()


        weather_data = {
            "city": city,
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "pressure": data["main"]["pressure"],
            "description": data["weather"][0]["description"],  
            "wind_speed": data["wind"]["speed"],
            "datetime": datetime.now()
        }

        print(f"Successfully fetched weather data for {city}")
        return weather_data

    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")
        raise
