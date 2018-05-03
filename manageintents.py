import json

intentsFile = open('intents.json')
intentsContent = intentsFile.read()

intents = json.loads(intentsContent)

toQuit = False
while not toQuit:
    print("List intents [l]; Quit [q]")
    command = input("> ")
    if command == "l":
        print("All skills:")
        for i in intents:
            print(i['name'])
    elif command == "q":
        print("Bye.")
        toQuit = True
