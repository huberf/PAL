import forecaster as weather
import os

myWeather = weather.Weather(os.environ['DARK_SKY_KEY'])
print myWeather.Request('0,0')
