import requests
from fake_useragent import UserAgent

from bot.config_data.config import settings


# For temperature in Celsius use units=metric


# &lang=ru  output in your language.
def get_weather(lati, long):
    ua = UserAgent()
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        "cache-control": "max-age=0",
        "connection": "keep-alive",
        "cookie": "signed_in=Serg",
        "dnt": "1",
        "host": "api.openweathermap.org",
        "sec-ch-ua": '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "Linux",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "none",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": ua.chrome,
    }
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lati}&lon={long}&units=metric&appid={settings.bot.api_token_weather}"
    try:
        response = requests.get(url=url, timeout=2, headers=headers)
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
