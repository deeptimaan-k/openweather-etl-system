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

import os

def save_to_csv(df):
    output_dir = "output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    df.to_csv(os.path.join(output_dir, "cleaned_weather.csv"), index=False)
    print("Data saved to cleaned_weather.csv successfully!")
