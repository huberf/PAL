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
    try:
        regex = i['regex']
    except:
        regex = []
    intent = generator.init(name, verbage, optional, regex)
    for z in verbage:
        for a in z[1]:
            engine.register_entity(a, z[0])
    for z in optional:
        for a in z[1]:
            engine.register_entity(a, z[0])
    try:
        for z in i['regex']:
            for a in z[1]:
                engine.register_regex_entity(a)
    except:
        # No regex included
        do_nothing = True
    engine.register_intent_parser(intent)

def process(text):
    global engine
    none_applicable = True
    #print(list(engine.determine_intent(text)))
    for intent in engine.determine_intent(text):
        if intent and intent.get('confidence') > 0:
            none_applicable = False
            return intent
    return None #{"intent_type": "None"}


if __name__ == "__main__":
    for intent in engine.determine_intent(' '.join(sys.argv[1:])):
        if intent and intent.get('confidence') > 0:
            print(json.dumps(intent, indent=4))

# To be tested upon import of file
is_working = True
