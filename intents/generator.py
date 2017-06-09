def init(name, verbage, optional, regex):
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

    intent = IntentBuilder(name)
    for i in verbage:
        intent = intent.require(i[0])
    for i in optional:
        intent = intent.optionally(i[0])
    for i in regex:
        intent = intent.require(i[0])
    intent = intent.build()

    is_working = True

    return intent
