from la_nlp import config
from spacy.tokens import Doc, Span, Token
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

ANALYZER = SentimentIntensityAnalyzer()
ASPECTS = config.get_aspects()
KEYWORDS = []
for KEYWORDS_LIST in ASPECTS.values():
    KEYWORDS.extend(KEYWORDS_LIST)

def set_extension(extension_name, default=None, target_obj=Doc):
    if not target_obj.has_extension(extension_name):
        target_obj.set_extension(extension_name, default=default)

def contains_aspect(doc):
    set_extension('contains_aspect', default=False)
    
    for token in doc:
        if token.lemma_.lower() in KEYWORDS:
            doc._.contains_aspect = True
            break
    
    return doc

def aspects_contained(doc):
    set_extension('aspects_contained')
    
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
    set_extension('keywords')

    if doc._.contains_aspect == True:
        keywords = []
        for token in doc:
            if token.lemma_.lower() in KEYWORDS:
                keywords.append(token)
        doc._.keywords = keywords
    return doc

def parent_span(doc):
    set_extension('parent_span', target_obj=Token)

    for token in doc:
        head = token.head
        siblings = head.children
        indices = [token.i for token in siblings]
        indices.append(head.i)
        indices.sort()
        first = indices[0]
        last = indices[-1] + 1
        if last >= len(doc):
            span = doc[first:]
        else:
            span = doc[first:last]
        token._.parent_span = span          

    return doc

def parent_span_sentiment(doc, include_non_keywords=False):
    set_extension('sentiment', target_obj=Span)

    if include_non_keywords == True:
        tokens = doc
    else:
        tokens = doc._.keywords
    
    if tokens == None:
        return doc
    
    for token in tokens:
        scores = ANALYZER.polarity_scores(token._.parent_span.text)
        sentiment = scores['compound']
        token._.parent_span._.sentiment = sentiment
    
    return doc

def aspect_sentiments(doc):
    set_extension('aspect_sentiments')

    aspect_sentiments = {aspect:None for aspect in ASPECTS}

    for aspect in doc._.aspects_contained:
        scores = []
        for keyword in ASPECTS[aspect]:
            scores.append(keyword._.parent_span._.sentiment)
        sentiment = sum(scores) / len(scores)
        aspect_sentiments[aspect] = sentiment
    
    doc._.aspect_sentiments = aspect_sentiments

    return doc
