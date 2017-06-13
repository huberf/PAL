import requests as r
import os
import voice

def weatherIntent(params):
    import weather
    return weather.actuate(params)

def startIntent(params):
    return "Application not supported yet."

def switchIntent(params):
    toReturn = 'Switching ' + params['Item'] + ' ' + params['Application']
    cmd = 'SPEAK.VOICE_ON'
    if params['Item'] == 'voice':
        if params['Application'] == 'on':
            if params['SPEAK.VOICE_STATUS']:
                toReturn = 'My voice is already on.'
            else:
                speak = True
        elif params['Application'] == 'off':
            cmd = 'SPEAK.VOICE_OFF'
            if params['SPEAK.VOICE_STATUS']:
                speak = False
            else:
                toReturn = 'My voice is already off.'
    else:
        toReturn = 'Desired item can\'t be controlled.'
    return {'message': toReturn, 'cmd': cmd}

def lastFMCount(params):
    toReturn = 'Sorry. I don\'t support that period.'
    try:
        if params['Period'] == 'today':
            period = 'today'
        else:
            toReturn = 'Unfortunately I don\'t support the provided period.'
    except:
        # Default to today if no period is specified
        period = 'today'
    if period == 'today':
        import lastfm
        output = lastfm.today_count()
        toReturn = 'You have scrobbled ' + str(output['dailyCount']) + ' tracks. ' + str(output['expectedCount']) + ' scrobbles expected.'
    return toReturn

def simonSays(params):
    voice.speak(params['Text'])
    return 'Speaking: ' + params['Text']

def shellExecute(params):
    os.system(params['Command'])
    return 'Command executed.'

def testIntent(params):
    print(params)
    return 'Test complete'

functions = {
        'WeatherIntent': weatherIntent,
        'StartIntent': startIntent,
        'SwitchIntent': switchIntent,
        'LastFMCount': lastFMCount,
        'SimonSays': simonSays,
        'ShellExecute': shellExecute,
        'TestIntent': testIntent
        }
