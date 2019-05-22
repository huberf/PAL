import forecaster as w
import os
myWeather = w.Weather(os.environ['DARK_SKY_KEY'])

def actuate(info):
  gpsData = info['LOCATION.GPS']
  coordinates = gpsData['current_location']['latlong']
  response = ""
  weather  =  myWeather.current(coordinates)
  if info["WeatherKeyword"] == "weather":
    distance = weather["nearestStormDistance"]
    if(distance < 5):
      response += "Storm nearby. Batten the hatches."
    response += "It is " + str(weather["summary"]) + " outside and is " + str(weather["temperature"]) + " with a humidity of " + str(weather["humidity"]) + " and a wind speed of " + str(weather["windSpeed"])
  elif info["WeatherKeyword"] == "humidity":
    response += "The humidity is " + str(weather["humidity"])
  return response
