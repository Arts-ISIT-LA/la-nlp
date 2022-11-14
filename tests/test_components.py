from la_nlp import components as comp
from spacy import load as load_model
from spacy.tokens import Doc
import pytest

TEST_TEXT_1 = """
This is a text that contains keyword1.
"""

ASPECTS = {'aspect1':['keyword1']}
KEYWORDS = ['keyword1']

@pytest.fixture
def nlp():
    nlp = load_model('en_core_web_lg')
    return nlp

def test_function_get_token_parent_span(nlp):
    text = "Hello world!"
    doc = nlp(text)
    assert comp.get_token_parent_span(doc[0]).text == text

def test_function_contains_aspect(nlp):
    doc = nlp(TEST_TEXT_1)
    doc = comp.contains_aspect(doc, base_keywords=KEYWORDS)
    assert doc._.contains_aspect is not None

def test_function_aspects(nlp):
    doc = nlp(TEST_TEXT_1)
    doc = comp.contains_aspect(doc, base_keywords=KEYWORDS)
    doc = comp.aspects(doc, base_aspects=ASPECTS)
    assert doc._.aspects is not None

def test_function_keywords(nlp):
    doc = nlp(TEST_TEXT_1)
    doc = comp.contains_aspect(doc, base_keywords=KEYWORDS)
    doc = comp.keywords(doc, base_keywords=KEYWORDS)
    assert doc._.keywords is not None

def test_function_keyword_aspects(nlp):
    doc = nlp(TEST_TEXT_1)
    doc = comp.contains_aspect(doc, base_keywords=KEYWORDS)
    doc = comp.keywords(doc, base_keywords=KEYWORDS)
    doc = comp.keyword_aspects(doc, base_aspects=ASPECTS)
    assert doc._.keywords[0]._.aspect is not None

def test_function_parent_span(nlp):
    doc = nlp(TEST_TEXT_1)
    doc = comp.contains_aspect(doc, base_keywords=KEYWORDS)
    doc = comp.keywords(doc, base_keywords=KEYWORDS)
    doc = comp.parent_span(doc)
    token1 = doc._.keywords[0]
    token2 = doc[1]
    assert token1._.parent_span is not None
    assert token2._.parent_span is None

def test_function_parent_span_non_keywords(nlp):
    doc = nlp(TEST_TEXT_1)
    doc = comp.parent_span(doc, include_non_keywords=True)
    assert doc[0]._.parent_span is not None

def test_function_parent_span_sentiment(nlp):
    doc = nlp(TEST_TEXT_1)
    doc = comp.contains_aspect(doc, base_keywords=KEYWORDS)
    doc = comp.keywords(doc, base_keywords=KEYWORDS)
    doc = comp.parent_span(doc)
    doc = comp.parent_span_sentiment(doc)
    token = doc._.keywords[0]
    assert token._.parent_span._.sentiment is not None

def test_function_parent_span_sentiment_non_keywords(nlp):
    doc = nlp(TEST_TEXT_1)
    doc = comp.parent_span(doc, include_non_keywords=True)
    doc = comp.parent_span_sentiment(doc, include_non_keywords=True)
    assert doc[0]._.parent_span._.sentiment is not None

def test_function_aspect_sentiments(nlp):
    doc = nlp(TEST_TEXT_1)
    doc = comp.contains_aspect(doc, base_keywords=KEYWORDS)
    doc = comp.keywords(doc, base_keywords=KEYWORDS)
    doc = comp.keyword_aspects(doc, base_aspects=ASPECTS)
    doc = comp.parent_span(doc)
    doc = comp.parent_span_sentiment(doc)
    doc = comp.aspect_sentiments(doc, base_aspects=ASPECTS)
    assert doc._.aspect_sentiments is not None
