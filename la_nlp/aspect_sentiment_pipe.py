from la_nlp import components, config
from spacy import load as load_model
from spacy.language import Language

ASPECTS = config.get_aspects()
KEYWORDS = []
for KEYWORDS_LIST in ASPECTS.values():
    KEYWORDS.extend(KEYWORDS_LIST)

NLP = load_model('en_core_web_lg')

def make_doc(text, nlp=NLP):
    return nlp(text, component_cfg={'aspect_sentiment_pipe':{'base_aspects':ASPECTS, 'base_keywords':KEYWORDS}})

@Language.component('aspect_sentiment_pipe')
def aspect_sentiment_pipe(doc, base_aspects, base_keywords):
    doc = components.contains_aspect(doc, base_keywords)
    doc = components.aspects(doc, base_aspects)
    doc = components.keywords(doc, base_keywords)
    doc = components.keyword_aspects(doc, base_aspects)
    doc = components.parent_span(doc)
    doc = components.parent_span_sentiment(doc)
    doc = components.aspect_sentiments(doc, base_aspects)
    return doc

NLP.add_pipe('aspect_sentiment_pipe')