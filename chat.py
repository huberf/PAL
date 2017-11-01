# Operation vars and funcs
failsafe = False
offline = False

import intent
import voice
import sys
import os
import time
import requests as r
import json
import mechanics

if not offline:
    config = json.load(open('config.json'))
else:
    config = json.load(open('offline.json'))
deactivated_skills = config['deactivated-skills']

# Load intent data
intents = json.load(open('intents.json'))

# Load addtional user data
gps_info = json.load(open('data/gps.json'))

# Variable area
claraLocation = config['servers']['clara']['url']
speak = False

# Handles loading of requirements and permissions
def load_additional_config(intentName):
    intent = None
    for i in intents:
        if i['name'] == intentName:
            intent = i
            break
    to_return = {}
    try:
        permissions = intent['permissions']
        for i in permissions:
            if i == 'STRAVA_KEYS':
                to_return.update(config['keys']['strava'])
            if i == 'TODOIST_KEY':
                to_return.update(config['keys']['todoist'])
    except:
        # No special information needed
        do_nothing = True
    return to_return

# Utility functions
def query_user(message):
    print(message)
    if speak:
        voice.speak(message)
    response = raw_input('> ')
    return response

def query_clara(text):
    data = {'input': text}
    rawResp = r.post(claraLocation + 'converse', json=data).text
    resp = json.loads(rawResp)
    return resp

def process(text):
    global speak, claraLocation, query_user
    action = intent.process(text)
    toReturn = 'None'
    image = 'None'
    if action == None:
        # Chat mode
        resp = query_clara(text)
        toReturn = resp['message']
        image = resp['image']
    else:
        params = action
        params.update({'SPEAK.VOICE_STATUS': speak, 'IO.QUERY_USER': query_user, 'CLARA.QUERY': query_clara, 'QUERY': text, 'LOCATION.GPS': gps_info});
        if not action['intent_type'] in deactivated_skills:
            additional_params = load_additional_config(action['intent_type'])
            params.update(additional_params)
            output = mechanics.functions[action['intent_type']](action)
        else:
            output = 'Unfortunately, the skill requested doesn\'t work with your current setup.'
        if isinstance(output, (str, unicode)):
            toReturn = output
        else:
            toReturn = output['message']
            if output['cmd'] == 'SPEAK.VOICE_ON':
                speak = True
            elif output['cmd'] == 'SPEAK.VOICE_OFF':
                speak = False
    return {'message': toReturn, 'image': image}

if __name__ == '__main__':
    exit = False
    while not exit:
        query = raw_input('> ')
        if query.lower() == 'quit':
            exit = True
        returned = {}
        if failsafe:
            try:
                returned = process(query)
            except:
                returned = {'message': 'Unable to perform desired action. Processing error occured.', 'image': 'None'}
        else:
            returned = process(query)
        print(returned['message'])
        if speak:
            voice.speak(returned['message'])
