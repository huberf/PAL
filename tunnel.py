from socketIO_client import SocketIO, LoggingNamespace
import os
import json
import voice

import mechanics

config = json.loads(open('config.json').read())

myId = config['identities']['pal-command']

def execute(data):
    success = True
    params = data['command']['params']

    output = mechanics.functions[params['intent_type']](params)

    if success:
        socketIO.emit('complete', {'clientId': myId, 'id': data['id'], 'response': output})

def on_handshake(data):
   print(data)
   for i in data['commands']:
       if not i == None:
           execute(i)

def on_command(data):
    print(data)
    execute(data)

dataFile = open('config.json')
config = json.load(dataFile)
socketIO = SocketIO(config['servers']['pal-command']['server'], config['servers']['pal-command']['port'], LoggingNamespace)
socketIO.on('handshake', on_handshake)
socketIO.on('command', on_command)

# Listen
socketIO.emit('handshake', {'id': myId})
socketIO.wait(seconds=1)

# Listen only once
while True:
    socketIO.wait(seconds=1)
