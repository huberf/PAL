# This is a standards compliant client for the PAL Command server
# GitHub: https://github.com/huberf/pal-command

from socketIO_client import SocketIO, LoggingNamespace
import voice

myId = 'main-client'

def execute(data):
    success = True
    if data['command']['action'] == 'basic':
        print('The message is: ' + data['command']['text'])
    elif data['command']['action'] == 'speak':
        voice.speak(data['command']['text'])
    else:
        success = False
        print('Can\'t process specified action.')
        print(data)
    if success:
        socketIO.emit('complete', {'clientId': myId, 'id': data['id']})

def on_handshake(data):
   print(data)
   for i in data['commands']:
       if not i == None:
           execute(i)

def on_command(data):
    print(data)
    execute(data)

socketIO = SocketIO('localhost', 1999, LoggingNamespace)
socketIO.on('handshake', on_handshake)
socketIO.on('command', on_command)

# Listen
socketIO.emit('handshake', {'id': myId})
socketIO.wait(seconds=1)

# Listen only once
while True:
    socketIO.wait(seconds=1)
