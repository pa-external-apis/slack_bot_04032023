import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import requests

slack_app_secret = os.environ['slack_app_secret']
slack_bot_secret = os.environ['slack_bot_secret']
weather_secret = os.environ['weather_app_secret']

def get_weather(query):
    URL = f"https://api.openweathermap.org/data/2.5/weather?q={query}&units=imperial&appid={weather_secret}"
    response = requests.get(URL)
    weather_data = response.json()
    message = f"Current temperature *{weather_data['main']['temp']}F* \
Feels like *{weather_data['main']['feels_like']} F*, *{weather_data['weather'][0]['description']}* \
Humidity *{weather_data['main']['humidity']}%*"

    return message


app = App(token=slack_bot_secret)

@app.command("/weather")
def handle_weather_command(ack, respond, command):
    
    ack()
    query = command["text"]
    try:
        message = get_weather(query)
        respond(message)
    except Exception as e:
        respond(e)
        
handler = SocketModeHandler(app, app_token=slack_app_secret)

handler.start()