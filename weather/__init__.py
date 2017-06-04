import forecaster as w
import os
myWeather = w.Weather(os.environ['DARK_SKY_KEY'])

def actuate(info):
  response = ""
  weather  =  myWeather.current('35.1391218,-85.99808539999998')
  if info["WeatherKeyword"] == "weather":
    distance = weather["nearestStormDistance"]
    if(distance < 5):
      response += "Storm nearby. Batten the hatches."
    response += "It is " + str(weather["summary"]) + " outside and is " + str(weather["temperature"]) + " with a humidity of " + str(weather["humidity"]) + " and a wind speed of " + str(weather["windSpeed"])
  elif info["WeatherKeyword"] == "humidity":
    response += "The humidity is " + str(weather["humidity"])
  return response
