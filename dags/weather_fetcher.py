"""
Weather data fetcher module for Airflow DAG
"""
import requests
import json
from datetime import datetime

def fetch_weather_data(city, api_key):
    """
    Fetch weather data for a given city using the OpenWeatherMap API

    Args:
        city (str): City name
        api_key (str): OpenWeatherMap API key

    Returns:
        dict: Weather data including temperature, humidity, etc.
    """
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric"  # For temperature in Celsius
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raise exception for 4XX/5XX responses

        data = response.json()

        # Extract relevant information
        weather_data = {
            "city": city,
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "pressure": data["main"]["pressure"],
            "description": data["weather"][0]["description"],  # Changed from weather_description to description
            "wind_speed": data["wind"]["speed"],
            "datetime": datetime.now()  # Changed from timestamp to datetime and using datetime object
        }

        print(f"Successfully fetched weather data for {city}")
        return weather_data

    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")
        raise
