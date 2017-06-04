import datetime
from lastpy import extras

def today_count():
    data = extras.user_daily_tracks('nhuberfeely')
    count = data['recenttracks']['@attr']['total']
    dailyCount = count
# 9*60*60
    workday = 32400
    dayStart = datetime.datetime.today().replace(hour=0, minute=0, second=0, microsecond=0).strftime("%s")
    currentTotal = float(datetime.datetime.today().strftime("%s")) - (float(dayStart) + (8*60*60))
    ratio = workday/currentTotal
    expectedCount = int(int(count) * ratio)
    return {'dailyCount': dailyCount, 'expectedCount': expectedCount}
