import os
from la_nlp.pipes import aspect_sentiment as asp
from la_nlp import config
import pytest
from spacy.tokens import Doc

FILE_DIR = os.path.dirname(__file__)

ASPECTS_1_PATH = os.path.join(FILE_DIR, 'test_data', 'test_aspects_1.toml')
ASPECTS_1 = config.get_aspects(ASPECTS_1_PATH)

ASPECTS_2_PATH = os.path.join(FILE_DIR, 'test_data', 'test_aspects_2.toml')
ASPECTS_2 = config.get_aspects(ASPECTS_2_PATH)

TEST_TEXT_1 = """
I enjoyed the course, but the readings were too long and the professor was mean.
"""

TEST_TEXT_2 = """
This is a text that does not contain any target aspects.
"""

@pytest.fixture
def doc1():
    doc1 = asp.make_doc(TEST_TEXT_1, aspects=ASPECTS_1)
    return doc1

@pytest.fixture
def doc2():
    doc2 = asp.make_doc(TEST_TEXT_2, aspects=ASPECTS_1)
    return doc2

def test_make_doc(doc1):
    assertion1 = "Should be a spacy Doc object"
    assert isinstance(doc1, Doc), assertion1

    assertion2 = "Should have a length of 19"
    assert len(doc1) == 19, assertion2


def test_contains_aspect(doc1, doc2):
    assertion1 = "doc1 should return True"
    assert doc1._.contains_aspect == True, assertion1

    assertion2 = "doc2 should return False"
    assert doc2._.contains_aspect == False, assertion2

def test_aspects(doc1, doc2):
    assertion1 = "doc1 should contain 'course', 'content', and 'instructor'"
    doc1_aspects = ['course', 'content', 'instructor']
    assert doc1._.aspects == doc1_aspects, assertion1

    assertion2 = "doc2 should contain None"
    doc2_aspects = None
    assert doc2._.aspects == doc2_aspects, assertion2

def test_keywords(doc1, doc2):
    assertion1 = "doc1 should contain keyword %s"
    doc1_targets = ['course', 'reading', 'professor']
    doc1_keywords = [kw.lemma_.lower() for kw in doc1._.keywords]
    for target in doc1_targets:
        assert target in doc1_keywords, assertion1 % target
    
    assertion2 = "doc2 should contain no keywords"
    doc2_targets = None
    assert doc2._.keywords == doc2_targets, assertion2

def test_keyword_aspects(doc1):
    assertion = "%s aspect should be %s"
    target_aspects = ['course', 'content', 'instructor']
    for keyword, aspect in zip(doc1._.keywords, target_aspects):
        assert keyword._.aspect == aspect, assertion % (keyword.text, aspect)


def test_parent_span(doc1, doc2):
    assertion1 = "Span should read 'professor was mean'"
    doc1_target = 'professor was mean'
    token1 = doc1._.keywords[2]
    assert token1._.parent_span.text == doc1_target, assertion1

    assertion2 = "Span should read 'that does not contain any target aspects'"
    doc2_target = None
    token2 = doc2[-3]
    assert token2._.parent_span == doc2_target, assertion2

def test_parent_span_sentiment(doc1):
    assertion = "course parent span sentiment should be 0.2846"
    span = doc1._.keywords[0]._.parent_span
    target_sentiment = 0.2846

    assert span._.sentiment == target_sentiment, assertion

def test_aspect_sentiments(doc1):
    target_sentiments = {
        'course': 0.2846,
        'content': 0,
        'assignments':None,
        'tests':None,
        'instructor': 0,
    }
    assertion = f"Sentiment dict should look like: {target_sentiments}"

    assert doc1._.aspect_sentiments == target_sentiments, assertion
