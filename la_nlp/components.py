from la_nlp import config
from spacy.tokens import Doc, Span, Token

ASPECTS = config.get_aspects()
KEYWORDS = []
for keywords in ASPECTS.values():
    KEYWORDS.extend(keywords)

def contains_aspect(doc):
    if not Doc.has_extension('contains_aspect'):
        Doc.set_extension('contains_aspect', default=False)
    
    for token in doc:
        if token.lemma_.lower() in KEYWORDS:
            doc._.contains_aspect = True
            break
    
    return doc

def aspects_contained(doc):
    if not Doc.has_extension('aspects_contained'):
        Doc.set_extension('aspects_contained', default=None)
    
    if doc._.contains_aspect == True:
        aspects_contained = []
        for token in doc:
            for aspect in ASPECTS:
                if aspect in aspects_contained:
                    continue
                keywords = ASPECTS[aspect]
                if token.lemma_.lower() in keywords:
                    aspects_contained.append(aspect)
        doc._.aspects_contained = aspects_contained
    return doc

def keywords(doc):
    if not Doc.has_extension('keywords'):
        Doc.set_extension('keywords', default=None)

    if doc._.contains_aspect == True:
        keywords = []
        for token in doc:
            if token.lemma_.lower() in KEYWORDS:
                keywords.append(token)
        doc._.keywords = keywords

    return doc
