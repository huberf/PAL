# Operation vars and funcs
failsafe = True

import intent
import voice
import sys
import os
import time
import requests as r
import json
import mechanics

config = json.load(open('config.json'))

# Variable area
claraLocation = config['servers']['clara']['url']
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
    else:
        params = action
        params.update({'SPEAK.VOICE_STATUS': speak});
        output = mechanics.functions[action['intent_type']](action)
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
