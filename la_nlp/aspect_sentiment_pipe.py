from la_nlp.components import *
from spacy import load as load_model
from spacy.language import Language

NLP = load_model('en_core_web_lg')

def make_doc(text, nlp=NLP):
    return nlp(text)

@Language.component('aspect_sentiment_pipe')
def aspect_sentiment_pipe(doc):
    doc = contains_aspect(doc)
    doc = aspects_contained(doc)
    doc = keywords(doc)
    doc = parent_span(doc)
    return doc

NLP.add_pipe('aspect_sentiment_pipe')
