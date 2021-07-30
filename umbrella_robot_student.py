from pystubit_iot import *
from pyatcrobo2.parts import Servomotor, UltrasonicSensor
from pystubit.board import display, Image
import time, json

# Servomotor and Ultrasonic Sensor settings

#WIFI settings
WIFI_SSID = ""
WIFI_PWD = ""
response = wifi_connect(WIFI_SSID, WIFI_PWD, trytime=3)

CITY_ID = 1 # Hong Kong City ID

WORDS_FINE = {"No Rain", "Fine", "Sunny", "Clear", "Clearing", "Bright",
                "Fair", "Mild"}
WORDS_RAINY = {"Thunderstorms", "Thundershowers", "Storm", "Showers",
                "Heavy Showers", "Rainshower", "Occasional Showers",
                "Scattered Showers", "Isolated Showers", "Light Showers",
                "Freezing Rain", "Rain", "Drizzle", "Light Rain", "Squall"}
WORDS_CLOUDY = {"Cloudy", "Partly Cloudy", "Sunny Intervals",
                "Mostly Cloudy", "Partly Bright"}
WORDS_SNOWY = {"Snow", "Flurries", "Heavy Snow", "Snowfall", "Light Snow",
                "Blizzard", "Blowing Snow", "Hail", "Snow Showers",
                "Snowstorm", "Snowdrift"}

IMG_FINE = Image("01110:11111:11111:11111:01110:", color=(30, 10, 0))
IMG_RAINY = Image("00100:01110:11111:00100:01100:", color=(0, 10, 30))
IMG_CLOUDY = Image("00000:01110:11111:01110:00000:", color=(15, 15, 15))
IMG_SNOWY = Image("10101:01110:11011:01110:10101:", color=(30, 30, 30))
IMG_OTHER = Image("00000:00000:01110:00000:00000:", color=(10, 5, 15))

def give_umbrella():
    # ...

def get_icon(weather):
    # ...

def get_forecast():
    url_format = "https://worldweather.wmo.int/en/json/[City ID]_en.json"
    url = url_format.replace("[City ID]", str(CITY_ID))
    res = json.loads(get_request(url))
    weather = res["city"]["forecast"]["forecastDay"][0]["weather"]
    hi_temp = res["city"]["forecast"]["forecastDay"][0]["maxTemp"]
    lo_temp = res["city"]["forecast"]["forecastDay"][0]["minTemp"]
    img = get_icon(weather)
    display.show(img, delay=3000)
    display.scroll("Hi: " + hi_temp, delay=25, color=(31, 0, 0))
    display.scroll("Lo: " + lo_temp, delay=25, color=(0, 0, 31))
    if weather in WORDS_RAINY:
        give_umbrella()

# main program
