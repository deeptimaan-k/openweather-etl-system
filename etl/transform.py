import pandas as pd

def clean_weather_data(raw_data):
    records = []
    
    for entry in raw_data:
        record = {
            "city_name": entry.get("name"),
            "temperature": entry.get("main", {}).get("temp"),
            "humidity": entry.get("main", {}).get("humidity"),
            "weather_description": entry.get("weather", [{}])[0].get("description")
        }
        records.append(record)
    
    df = pd.DataFrame(records)
    return df
