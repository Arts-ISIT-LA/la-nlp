from la_nlp import components, utils
from spacy import load as load_model
from spacy.language import Language

ASPECTS = utils.get_aspects()

NLP = load_model('en_core_web_lg')

def make_doc(text, aspects=ASPECTS, parent_span_min_length=7):
    keywords = utils.get_keywords_from_aspects(aspects)
    
    cfg = {
        'aspect_sentiment_pipe': {
            'base_aspects': aspects,
            'base_keywords': keywords,
            'parent_span_min_length': parent_span_min_length, 
        }
    }
    return NLP(text, component_cfg=cfg)

@Language.component('aspect_sentiment_pipe')
def aspect_sentiment_pipe(doc, base_aspects, base_keywords, parent_span_min_length=7):
    doc = components.set_doc_contains_aspect(doc, base_keywords)
    doc = components.set_doc_aspects(doc, base_aspects)
    doc = components.set_doc_keywords(doc, base_keywords)
    doc = components.set_token_aspects(doc, base_aspects)
    doc = components.set_token_parent_span(doc, min_length=parent_span_min_length)
    doc = components.set_span_sentiment(doc)
    doc = components.set_doc_aspect_sentiments(doc, base_aspects)
    return doc

NLP.add_pipe('aspect_sentiment_pipe')
