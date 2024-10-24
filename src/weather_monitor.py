import requests
import time
import pandas as pd
from datetime import datetime
from config import API_KEY, LOCATIONS
weather_data = []

TEMP_THRESHOLD = 35  
alerts = []

def fetch_weather_data():
    """Fetch current weather data from OpenWeatherMap API."""
    for city in LOCATIONS:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            main = data['main']
            weather = {
                'city': city,
                'temp': main['temp'] - 273.15,  
                'feels_like': main['feels_like'] - 273.15,
                'dt': datetime.fromtimestamp(data['dt']),
                'condition': data['weather'][0]['main']
            }
            weather_data.append(weather)
            check_alerts(weather)
            print(f"Fetched data for {city}: {weather}")
        else:
            print(f"Failed to fetch data for {city}: {response.status_code}")

def check_alerts(weather):
    """Check if current weather exceeds predefined thresholds."""
    if weather['temp'] > TEMP_THRESHOLD:
        alerts.append(f"Alert! {weather['city']} temperature is {weather['temp']:.2f}°C.")

def process_weather_data():
    """Process the weather data to generate daily summaries."""
    df = pd.DataFrame(weather_data)
    if not df.empty:
        daily_summary = {
            'date': df['dt'].dt.date.iloc[0],
            'avg_temp': df['temp'].mean(),
            'max_temp': df['temp'].max(),
            'min_temp': df['temp'].min(),
            'dominant_condition': df['condition'].mode()[0]
        }
        print("Daily Summary:", daily_summary)

def main():
    """Main function to fetch and process weather data continuously."""
    while True:
        fetch_weather_data()
        process_weather_data()
        time.sleep(300)  # Sleep for 5 minutes before fetching again

if __name__ == "__main__":
    main()
