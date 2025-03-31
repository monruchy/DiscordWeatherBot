import requests
from datetime import datetime

WEATHER_API_KEY = ''
LAT = '14.5289'  # Latitude for Saraburi, Thailand      
LON = '100.9100'  # Longitude for Saraburi, Thailand  

def check_weather_api():
    weather_url = f"http://api.openweathermap.org/data/2.5/weather?q=Saraburi,TH&units=metric&appid={WEATHER_API_KEY}"
    response = requests.get(weather_url)
    if response.status_code == 200:
        print("Weather API Response:")
        print(response.json())
    else:
        print(f"Weather API Error: {response.status_code} - {response.text}")

def check_forecast_api():
    forecast_url = f"http://api.openweathermap.org/data/2.5/onecall?lat={LAT}&lon={LON}&exclude=minutely,hourly,alerts&units=metric&appid={WEATHER_API_KEY}"
    response = requests.get(forecast_url)
    if response.status_code == 200:
        print("Forecast API Response:")
        print(response.json())
    else:
        print(f"Forecast API Error: {response.status_code} - {response.text}")

def check_air_quality_api():
    air_quality_url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={LAT}&lon={LON}&appid={WEATHER_API_KEY}"
    response = requests.get(air_quality_url)
    if response.status_code == 200:
        print("Air Quality API Response:")
        print(response.json())
    else:
        print(f"Air Quality API Error: {response.status_code} - {response.text}")

if __name__ == "__main__":
    print("Checking Weather API...")
    check_weather_api()
    print("\nChecking Forecast API...")
    check_forecast_api()
    print("\nChecking Air Quality API...")
    check_air_quality_api()