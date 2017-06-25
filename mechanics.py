# Global configurations
remote = False
remoteMachine = 'main-client'

import requests as r
import json
import os
import voice

config = json.loads(open('config.json').read())
commandServer ='http://' + config['servers']['pal-command']['server'] + ':' + config['servers']['pal-command']['port'] + '/'

def weatherIntent(params):
    import weather
    return weather.actuate(params)

def startIntent(params):
    applications = json.loads(open('data/applications.json').read())
    foundApplication = False
    applicationName = None
    applicationPath = None
    for i in applications:
        for a in i['keywords']:
            if params['Application'] == a.lower():
                foundApplication = True
                applicationPath = i['path']
                applicationName = i['name']
                break
    if foundApplication:
        if remote:
            r.post(commandServer + 'add/' + remoteMachine, json={'command': {'action': 'open', 'path': applicationPath}})
        else:
            os.system('open ' + applicationPath)
    if not foundApplication:
        return "Application not supported yet."
    else:
        return "Launching application " + applicationName + '.'

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
    if remote:
        r.post(commandServer + 'add/' + remoteMachine, json={'command': {'action': 'speak', 'text': params['Text']}})
    else:
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
