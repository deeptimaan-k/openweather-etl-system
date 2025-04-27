CREATE TABLE weather_data (
    id SERIAL PRIMARY KEY,
    city_name VARCHAR(100),
    temperature FLOAT,
    humidity INTEGER,
    weather_description VARCHAR(255),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
