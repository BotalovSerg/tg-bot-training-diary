import requests

from bot.config_data.config import settings


# For temperature in Celsius use units=metric


# &lang=ru  output in your language.
def get_weather(lati, long):
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lati}&lon={long}&appid={settings.bot.api_token_weather}&units=metric"
    response = requests.get(url=url)
    print(response)