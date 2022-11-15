from la_nlp import components, config
from spacy import load as load_model
from spacy.language import Language

ASPECTS = config.get_aspects()

NLP = load_model('en_core_web_lg')

def make_doc(text, nlp=NLP, aspects=ASPECTS, parent_span_min_length=7):
    keywords = []
    for keywords_list in aspects.values():
        keywords.extend(keywords_list)
    
    cfg = {
        'aspect_sentiment_pipe': {
            'base_aspects': aspects,
            'base_keywords': keywords,
            'parent_span_min_length': parent_span_min_length, 
        }
    }
    return nlp(text, component_cfg=cfg)

@Language.component('aspect_sentiment_pipe')
def aspect_sentiment_pipe(doc, base_aspects, base_keywords, parent_span_min_length=7):
    doc = components.contains_aspect(doc, base_keywords)
    doc = components.aspects(doc, base_aspects)
    doc = components.keywords(doc, base_keywords)
    doc = components.keyword_aspects(doc, base_aspects)
    doc = components.parent_span(doc, min_length=parent_span_min_length)
    doc = components.parent_span_sentiment(doc)
    doc = components.aspect_sentiments(doc, base_aspects)
    return doc

NLP.add_pipe('aspect_sentiment_pipe')
