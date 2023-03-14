import requests
import os
from twilio.rest import Client
# The below import imports load_dotenv which will go over to twilio.env file and import its variables into os.environ
from dotenv import load_dotenv


# Loads variables into os.environ from external file
load_dotenv('twilio.env')


# Load Twilio Keys from os.environ
account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
auth_token = os.environ.get('TWILIO_AUTH_TOKEN')


# Load OpenWeatherMap key from os.environ
owm_endpoint = "https://api.openweathermap.org/data/2.5/onecall"
OWM_api_key = os.environ.get('OWM_API_KEY')

# ----------- MAKE SURE TO USE THE CORRECT LAT/LANG BELOW
parameters = {
    "lat":  32.6207,
    "lon": 35.5521,
    "exclude": "current,minutely,daily",
    "appid": OWM_api_key,
}
response = requests.get(owm_endpoint, params=parameters)
response.raise_for_status()
print(response.status_code)
hourly = response.json()["hourly"][:16]
send_alert = False

for hour_data in hourly:
    if hour_data["weather"][0]["id"] < 700:
        send_alert = True
        break

if send_alert:
    print("Bring an umbrella")
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body='Bring an umbrella☔️',
        from_='+YOU_TWILIO_NUMBER',
        to='+RECIPIENT_PHONE_NUMBER'
    )

    print(message.status)
