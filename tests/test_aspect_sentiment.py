from la_nlp.aspect_sentiment_pipe import *
import pytest

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from spacy.tokens import Doc


TEST_TEXT_1 = """
I enjoyed the course, but the readings were too long and the professor was mean.
"""

TEST_TEXT_2 = """
This is a text that does not contain any target aspects.
"""

@pytest.fixture
def doc1():
    doc1 = make_doc(TEST_TEXT_1)
    return doc1

@pytest.fixture
def doc2():
    doc2 = make_doc(TEST_TEXT_2)
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

def test_aspects_contained(doc1, doc2):
    assertion1 = "doc1 should contain 'course', 'content', and 'instructor'"
    doc1_aspects = ['course', 'content', 'instructor']
    assert doc1._.aspects_contained == doc1_aspects, assertion1

    assertion2 = "doc2 should contain None"
    doc2_aspects = None
    assert doc2._.aspects_contained == doc2_aspects, assertion2

def test_keywords(doc1, doc2):
    assertion1 = "doc1 should contain keyword %s"
    doc1_targets = ['course', 'reading', 'professor']
    doc1_keywords = [kw.lemma_.lower() for kw in doc1._.keywords]
    for target in doc1_targets:
        assert target in doc1_keywords, assertion1 % target
    
    assertion2 = "doc2 should contain no keywords"
    doc2_targets = None
    assert doc2._.keywords == doc2_targets, assertion2

def test_parent_span(doc1, doc2):
    assertion1 = "Span should read 'professor was mean'"
    doc1_target = 'professor was mean'
    token1 = doc1._.keywords[2]
    assert token1._.parent_span.text == doc1_target, assertion1

    assertion2 = "Span should read 'that does not contain any target aspects'"
    doc2_target = 'that does not contain any target aspects'
    token2 = doc2[-3]
    assert token2._.parent_span.text == doc2_target, assertion2

def test_parent_span_sentiment(doc1, doc2):
    assertion = "course parent span sentiment should be 0.286"
    span = doc1._.keywords[0]._.parent_span
    target_sentiment = 0.2846

    assert span._.sentiment == target_sentiment, assertion
