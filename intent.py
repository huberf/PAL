import json
import sys
from adapt.entity_tagger import EntityTagger
from adapt.tools.text.tokenizer import EnglishTokenizer
from adapt.tools.text.trie import Trie
from adapt.intent import IntentBuilder
from adapt.parser import Parser
from adapt.engine import IntentDeterminationEngine

tokenizer = EnglishTokenizer()
trie = Trie()
tagger = EntityTagger(trie, tokenizer)
parser = Parser(tokenizer, tagger)

engine = IntentDeterminationEngine()

# Lastfm today
intentsFile = open('intents.json')
intentsJson = json.loads(intentsFile.read())
import intents.generator as generator
for i in intentsJson:
    name = i['name']
    verbage = i['verbage']
    optional = i['optional']
    intent = generator.init(name, verbage, optional)
    for i in verbage:
        for a in i[1]:
            engine.register_entity(a, i[0])
    for i in optional:
        for a in i[1]:
            engine.register_entity(a, i[0])
    engine.register_intent_parser(intent)

def process(text):
    global engine
    for intent in engine.determine_intent(text):
        if intent and intent.get('confidence') > 0:
            return intent
        else:
            return {"intent_type": "None"}


if __name__ == "__main__":
    for intent in engine.determine_intent(' '.join(sys.argv[1:])):
        if intent and intent.get('confidence') > 0:
            print(json.dumps(intent, indent=4))

# To be tested upon import of file
is_working = True
