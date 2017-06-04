import requests as r
import os
import json

url = "https://api.forecast.io/forecast/" + os.environ['DARK_SKY_KEY']

class Weather:
  api = ""
  def __init__(self, api_key):
    self.api = "https://api.forecast.io/forecast/" + api_key + "/"
  def Request(self, location):
    request = r.get(self.api + location)
    data = json.loads(request.text)
    return data
  def test(self):
    data = Request('0,0')
    print data['currently']
  def current(self, location):
    data = self.Request(location)
    return data['currently']
  def summary(self, location):
    data = self.hourly(location)
    return data['summary']
  def hourly(self, location):
    data = self.Request(location)
    return data['hourly']
  def stormDistance(self, location):
    data = self.current(location)
    return data['nearestStormDistance']
