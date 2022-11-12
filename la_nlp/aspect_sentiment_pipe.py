from la_nlp import config
from spacy import load as load_model
from spacy.language import Language
from spacy.tokens import Doc, Span, Token

ASPECTS = config.get_aspects()
NLP = load_model('en_core_web_lg')

def make_doc(text, nlp=NLP):
    return nlp(text)

@Language.component('contains_aspect')
def contains_aspect(doc):
    if not Doc.has_extension('contains_aspect'):
        Doc.set_extension('contains_aspect', default=False)

    aspect_keywords = []
    for keywords in ASPECTS.values():
        aspect_keywords.extend(keywords)
    
    for token in doc:
        if token.lemma_.lower() in aspect_keywords:
            doc._.contains_aspect = True
            break
    
    return doc

@Language.component('aspects_contained')
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


NLP.add_pipe('contains_aspect', last=True)
NLP.add_pipe('aspects_contained', last=True)