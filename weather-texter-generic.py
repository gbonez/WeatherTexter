import os
import requests
from twilio.rest import Client

# Fetch data from environment variables
weather_api_key = os.environ['WEATHER_API_KEY']
city_id = os.environ['CITY_ID']

# Twilio Configuration from environment
twilio_account_sid = os.environ['TWILIO_ACCOUNT_SID']
twilio_auth_token = os.environ['TWILIO_AUTH_TOKEN']
twilio_phone_number = os.environ['TWILIO_PHONE_NUMBER']
receiver_phone_number = os.environ['RECEIVER_PHONE_NUMBER']

# Preferred units can be hard coded or set via environment as needed
units = 'imperial'

# OpenWeatherMap API URL
url = f'https://api.openweathermap.org/data/2.5/weather?id={city_id}&units={units}&appid={weather_api_key}'

# Send an SMS with the weather information
def send_weather_sms(weather_data):
    city_name = weather_data["name"]
    
    client = Client(twilio_account_sid, twilio_auth_token)
    
    message = client.messages.create(
        body=f'The weather in {city_name} is {weather_data["main"]["temp"]}°F with {weather_data["weather"][0]["description"]}.',
        from_=twilio_phone_number,
        to=receiver_phone_number
    )
    
    print(f'SMS sent with SID: {message.sid}')

# Get weather data from OpenWeatherMap
try:
    response = requests.get(url)
    data = response.json()
    
    city_name = data["name"]
    
    print(f'Request URL for {city_name}: {url}')
    
    if response.status_code == 200:
        send_weather_sms(data)
    else:
        print(f'Failed to fetch weather data for {city_name}. HTTP Status Code: {response.status_code}, Response: {data}')
except Exception as e:
    print(f'An error occurred: {str(e)}')
