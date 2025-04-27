---
title: Building a Robust ETL Pipeline for Weather Data Using Python and Supabase
published: false
description: Learn how to build a complete ETL pipeline that extracts weather data from OpenWeatherMap API, transforms it with Pandas, and loads it into a Supabase PostgreSQL database.
tags: python, data, etl, tutorial
cover_image: 
series: 
---

# Building a Robust ETL Pipeline for Weather Data Using Python and Supabase

In today's data-driven world, ETL (Extract, Transform, Load) pipelines are crucial for collecting, cleaning, and storing data efficiently. In this tutorial, I'll walk you through a practical ETL project that fetches live weather data from the OpenWeatherMap API, transforms it, and loads it into a PostgreSQL database hosted on Supabase — all with Python!

## What You'll Learn

- How to extract real-time weather data using OpenWeatherMap API
- Cleaning and transforming JSON data into a structured format using Pandas
- Loading clean data into a cloud-hosted PostgreSQL database using psycopg2
- Best practices for environment management and code organization

## Why This Project?

Weather data powers many applications — from travel planning to agriculture. Having a reliable pipeline to gather and store such data helps businesses build intelligent features and dashboards.

I chose Supabase for the database because it offers a scalable, managed Postgres backend with easy authentication and dashboard tools. Python is the glue for fetching, processing, and loading data.

## Project Overview

Here's the high-level flow:

1. **Extract**: Fetch current weather data for multiple cities from the OpenWeatherMap API
2. **Transform**: Parse the JSON, clean the data, and convert it into a Pandas DataFrame
3. **Load**: Insert the cleaned data into a PostgreSQL table on Supabase and save a CSV backup

## Setting Up the Environment

Before starting, make sure you have:

- Python 3.8+ installed
- A Supabase account and project with PostgreSQL database created
- An OpenWeatherMap API key (free tier available)

Create a `.env` file for your secrets:

```
OPENWEATHER_API_KEY=your_openweather_api_key_here
DB_HOST=your_supabase_db_host
DB_PORT=6543
DB_NAME=your_supabase_db_name
DB_USER=your_supabase_db_user
DB_PASSWORD=your_supabase_db_password
```

Install dependencies:

```bash
pip install psycopg2-binary pandas requests python-dotenv
```

## Step 1: Extract - Fetching Weather Data

Using the OpenWeatherMap API, we query current weather for a list of cities. The API returns rich JSON data which we save locally as a raw backup.

```python
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
```

## Step 2: Transform - Cleaning and Structuring Data

Raw JSON is difficult to analyze directly. We extract key fields like city name, temperature, humidity, and weather description, and convert this into a Pandas DataFrame for easy handling.

```python
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
```

## Step 3: Load - Storing Data in Supabase PostgreSQL

Using psycopg2, we connect to the Supabase PostgreSQL database and insert our cleaned records. We also save a CSV backup locally.

```python
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def load_to_database(df):
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            port=os.getenv("DB_PORT")
        )
        cur = conn.cursor()
        
        for _, row in df.iterrows():
            cur.execute("""
                INSERT INTO weather_data (city_name, temperature, humidity, weather_description)
                VALUES (%s, %s, %s, %s)
            """, (row['city_name'], row['temperature'], row['humidity'], row['weather_description']))
        
        conn.commit()
        cur.close()
        conn.close()
        print("Data loaded into Supabase database successfully!")
        
    except Exception as e:
        print(f"Error loading data into database: {e}")

def save_to_csv(df):
    output_dir = "output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    df.to_csv(os.path.join(output_dir, "cleaned_weather.csv"), index=False)
    print("Data saved to cleaned_weather.csv successfully!")
```

## Putting It All Together

Finally, our main pipeline script runs the steps in sequence, and logs the process:

```python
from etl.extract import fetch_weather_data
from etl.transform import clean_weather_data
from etl.load import load_to_database, save_to_csv
import logging

logging.basicConfig(
    filename='logs/etl.log',
    level=logging.INFO,
    format='%(asctime)s:%(levelname)s:%(message)s'
)

def main():
    logging.info("ETL pipeline started.")
    
    cities = ["New York", "London", "Tokyo", "Delhi", "Sydney"]
    raw_data = fetch_weather_data(cities)
    cleaned_data = clean_weather_data(raw_data)
    load_to_database(cleaned_data)
    save_to_csv(cleaned_data)
    
    logging.info("ETL pipeline completed successfully.")

if __name__ == "__main__":
    main()
```

## Final Thoughts

This project demonstrates a full end-to-end ETL pipeline using real APIs and cloud databases. It's easily extendable — you can add more cities, schedule the script to run periodically, or build a dashboard on top of your Supabase data.

Check out the [OpenWeather ETL System](https://github.com/deeptimaan-k/openweather-etl-system) for complete source code and setup instructions.

Happy coding! 🚀