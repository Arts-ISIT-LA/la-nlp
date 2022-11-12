from la_nlp.aspect_sentiment_pipe import *

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from spacy.tokens import Doc


TEST_TEXT_1 = """
I enjoyed the course, but the readings were too long and the professor was mean.
"""

TEST_TEXT_2 = """
This is a text that does not contain any target aspects.
"""

def test_make_doc():
    doc = make_doc(TEST_TEXT_1)

    assertion1 = "Should be a spacy Doc object"
    assert isinstance(doc, Doc), assertion1

    assertion2 = "Should have a length of 19"
    assert len(doc) == 19, assertion2


def test_contains_aspect():
    doc1 = make_doc(TEST_TEXT_1)
    doc2 = make_doc(TEST_TEXT_2)

    assertion1 = "doc1 should return True"
    assert doc1._.contains_aspect == True

    assertion1 = "doc2 should return False"
    assert doc2._.contains_aspect == False

def test_aspects_contained():
    doc1 = make_doc(TEST_TEXT_1)
    doc2 = make_doc(TEST_TEXT_2)

    assertion1 = "doc1 should contain 'course', 'content', and 'instructor'"
    doc1_aspects = ['course', 'content', 'instructor']
    assert doc1._.aspects_contained == doc1_aspects, assertion1

    assertion2 = "doc2 should contain None"
    doc2_aspects = None
    assert doc2._.aspects_contained == doc2_aspects, assertion2
