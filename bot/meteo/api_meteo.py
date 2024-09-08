import requests

from bot.config_data.config import settings


# For temperature in Celsius use units=metric


# &lang=ru  output in your language.
def get_weather(lati, long):
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lati}&lon={long}&appid={settings.bot.api_token_weather}&units=metric"
    try:
        response = requests.get(url=url, timeout=2)
        data = response.json()
        return data["main"]
    except Exception as e:
        print(e)
        return


# {
#     "coord": {"lon": 63.0461, "lat": 57.6814},
#     "weather": [
#         {"id": 804, "main": "Clouds", "description": "overcast clouds", "icon": "04d"}
#     ],
#     "base": "stations",
#     "main": {
#         "temp": 16.41,
#         "feels_like": 15.7,
#         "temp_min": 16.41,
#         "temp_max": 16.41,
#         "pressure": 1017,
#         "humidity": 61,
#         "sea_level": 1017,
#         "grnd_level": 1009,
#     },
#     "visibility": 10000,
#     "wind": {"speed": 3.75, "deg": 301, "gust": 6.85},
#     "clouds": {"all": 92},
#     "dt": 1725622810,
#     "sys": {"country": "RU", "sunrise": 1725584369, "sunset": 1725633192},
#     "timezone": 18000,
#     "id": 1505526,
#     "name": "Irbit",
#     "cod": 200,
# }
