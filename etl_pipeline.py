from etl.extract import fetch_weather_data
from etl.transform import clean_weather_data
from etl.load import load_to_database, save_to_csv
import logging

# Setup logging
logging.basicConfig(
    filename='logs/etl.log',
    level=logging.INFO,
    format='%(asctime)s:%(levelname)s:%(message)s'
)

def main():
    logging.info("ETL pipeline started.")
    
    # List of cities
    cities = ["New York", "London", "Tokyo", "Delhi", "Sydney"]
    
    # Extract
    raw_data = fetch_weather_data(cities)
    
    # Transform
    cleaned_data = clean_weather_data(raw_data)
    
    # Load
    load_to_database(cleaned_data)
    save_to_csv(cleaned_data)
    
    logging.info("ETL pipeline completed successfully.")

if __name__ == "__main__":
    main()
