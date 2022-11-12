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


NLP.add_pipe('contains_aspect', last=True)