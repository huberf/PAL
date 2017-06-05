import intent
import voice
import sys
import os
import time
import requests as r
import json

# Variable area
claraLocation = os.environ['CLARA_SERVER']
speak = False

def process(text):
    global speak, claraLocation
    action = intent.process(text)
    toReturn = 'None'
    image = 'None'
    if action == None:
        # Chat mode
        data = {'input': text}
        rawResp = r.post(claraLocation + 'converse', json=data).text
        resp = json.loads(rawResp)
        toReturn = resp['message']
        image = resp['image']
    elif action["intent_type"] == "WeatherIntent":
        import weather
        response = weather.actuate(action)
        toReturn = response
    elif action["intent_type"] == "StartIntent":
        toReturn = "Action not support yet."
    elif action['intent_type'] == 'SwitchIntent':
        toReturn = 'Switching ' + action['Item'] + ' ' + action['Application']
        if action['Item'] == 'voice':
            if action['Application'] == 'on':
                if speak:
                    toReturn = 'My voice is already on.'
                else:
                    speak = True
            elif action['Application'] == 'off':
                if speak:
                    speak = False
                else:
                    toReturn = 'My voice is already off.'
        else:
            toReturn = 'Desired item can\'t be controlled.'
    elif action['intent_type'] == 'LastFMCount':
        try:
            if action['Period'] == 'today':
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
    else:
        toReturn = "No action specified"
    return {'message': toReturn, 'image': image}

if __name__ == '__main__':
    exit = False
    while not exit:
        query = raw_input('> ')
        if query.lower() == 'quit':
            exit = True
        try:
            returned = process(query)
        except:
            returned = {'message': 'Unable to perform desired action. Processing error occured.', 'image': 'None'}
        print(returned['message'])
        if speak:
            voice.speak(returned['message'])
