from la_nlp import components
from spacy import load as load_model
from spacy.language import Language

NLP = load_model('en_core_web_lg')

def make_doc(text, nlp=NLP):
    return nlp(text)

@Language.component('aspect_sentiment_pipe')
def aspect_sentiment_pipe(doc):
    doc = components.aspects(doc)
    doc = components.contains_aspect(doc)
    doc = components.keywords(doc)
    doc = components.keyword_aspects(doc)
    doc = components.parent_span(doc)
    doc = components.parent_span_sentiment(doc)
    doc = components.aspect_sentiments(doc)
    return doc

NLP.add_pipe('aspect_sentiment_pipe')
