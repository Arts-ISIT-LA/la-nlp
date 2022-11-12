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
    doc1_keywords = ['course', 'reading', 'professor']
    for keyword in doc1._.keywords:
        kw = keyword.lemma_.lower()
        assert kw in doc1_keywords, assertion1 % kw
    
    assertion2 = "doc2 should contain no keywords"
    doc2_keywords = None
    assert doc2._.keywords == doc2_keywords, assertion2


def test_aspect_spans(doc1, doc2):
    assert True
