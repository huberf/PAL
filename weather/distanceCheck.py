import forecaster as w
myWeather = w.Weather(os.environ['DARK_SKY_KEY'])
distance = myWeather.stormDistance('35.1391218,-85.99808539999998')
if(distance < 5):
  print "Storm nearby. Batten the hatches."
else:
  print "No storm nearby, but keep your eyes open."
