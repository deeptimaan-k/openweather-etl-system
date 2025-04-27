import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

def fetch_weather_data(cities):
    all_weather_data = []
    
    for city in cities:
        params = {
            "q": city,
            "appid": API_KEY,
            "units": "metric"
        }
        response = requests.get(BASE_URL, params=params)
        if response.status_code == 200:
            data = response.json()
            all_weather_data.append(data)
        else:
            print(f"Failed to fetch weather data for {city}")
    
    # Save raw data
    with open('data/raw_weather.json', 'w') as f:
        json.dump(all_weather_data, f, indent=4)
        
    return all_weather_data
