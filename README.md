# Personal Assistant and Learner (PAL)

This tool is meant to provide any easy interface and solution for integrating
with your existing tools and automation functions while provide a feature
complete natural language processing engine that can determine intents while
also integrating with the Clara program for general purpose chatting.

# Overview
All intents are stored in `intents.json` and adding new ones is as easy as
adding a simple JSON string. You can setup a personal Clara instance at any
location so long as it is network accessible and then add the endpoint into the
PAL program, so you can say things like `What are you up to?`, `I'm feeling
burnt out.` and `You are awesome!` and PAL will be able to respond
appropriately.
Once you've added an intent to `intents.json`, you can now go into `chat.py` and
add an additional if statement for when the intent name matches the name you've
given your new intent. You can then add any logic you want below this if
statement.
Type `python chat.py` and you now have a fully working personal assistant. You
can also launch `web.py` to make the service network accessible. The `web.py`
file integrates with the Clara standard and can therefore be accessed through
the Clara mobile app.

# Setup
* First clone the repo at [to be added](/#)
* Now install all requirements in `requirements.txt`
* Run `python chat.py` and attempt typing `Launch vim`.
* If success, you can now do things such as get a Dark Sky API token and add is
  as an environement variable at `DARK_SKY_KEY`.
* It's also recommended to connect to a clara instance at the [Clara
  repo](https://github.com/huberf/clara-bot). If the Clara instance isn't local,
  you can modify `config.json` with the URL. To install Clara, run `pip install
  clara` and then in a directory of your choice, set up the system by typing
  `clara` and it will populate the needed files.
* If you use [last.fm](http://last.fm) you can also hook this up by editing the
  username in `lastfm.py`.
