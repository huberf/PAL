import json
# Global configurations
config = json.loads(open('config.json').read())
# This variable decides if commands are executed locally or on a remote machine
remote = config['remote']
remoteMachine = config['identities']['pal-command']

import requests as r
import os
import voice
import stocks

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

def todoistAdd(params):
    if not config['keys']['todoist'] == 'None':
        if not params['Text'] == None:
            dataToSend = {
                'token': config['keys']['todoist'],
                'text': params['Text']
                }
            try:
                dataToSend['text'] += ' ' + params['TodoistDate']
            except:
                doNothing = True
            r.post('https://todoist.com/API/v7/quick/add', dataToSend)
            return 'Task added to Todoist.'
        else:
            return 'Task addition failed due to lack of task text.'
    else:
        return 'You need to configure the Todoist skill with your Todoist API key.'

def stockSum(params):
    sumOfIt = stocks.netAssets()
    return 'Your current stock valuation is $' + str(sumOfIt) + '.'

def stockIncrease(params):
    profits = stocks.currentProfits()
    return 'Your current stock increase is $' + str(profits) + '.'

def nomieLog(params):
    nomieProxyServer = config['servers']['nomie-proxy']
    r.get(nomieProxyServer['url'] + nomieProxyServer['secret'] + '/' + params['NomieItem'])
    return 'I have logged that you ' + params['NomieItem'] + '.'

def nomieCount(params):
    nomieComputeServer = config['servers']['compute-nomie']
    data = json.loads(r.get(nomieComputeServer['url'] + 'count', { 'label': params['NomieTrackername'], 'start': 1 }).text)
    if data['success']:
        return 'The count for tracker ' + params['NomieTrackername'] + ' is ' + str(data['count'])
    else:
        return 'Server responded with a failure and the message ' + data['message']

def exerciseManager(params):
    try:
        strava_id = params['strava']['id']
        response = "Your ID is " + str(strava_id)
        return response
    except:
        return "Skill failure."

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
        'TodoistAdd': todoistAdd,
        'StockSum': stockSum,
        'StockIncrease': stockIncrease,
        'NomieLog': nomieLog,
        'NomieCount': nomieCount,
        'ExerciseManager': exerciseManager,
        'TestIntent': testIntent
        }
