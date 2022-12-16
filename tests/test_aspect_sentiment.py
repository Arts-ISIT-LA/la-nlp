"""Test functions for the la_nlp.pipes.aspect_sentiment module.
"""

import os
from la_nlp.pipes import aspect_sentiment as asp
from la_nlp import utils
import pytest
from spacy.tokens import Doc

FILE_DIR = os.path.dirname(__file__)

ASPECTS_1_PATH = os.path.join(FILE_DIR, "test_data", "test_aspects_1.toml")
ASPECTS_1 = utils.get_aspects_from_file(ASPECTS_1_PATH)

ASPECTS_2_PATH = os.path.join(FILE_DIR, "test_data", "test_aspects_2.toml")
ASPECTS_2 = utils.get_aspects_from_file(ASPECTS_2_PATH)

TEST_TEXT_1 = """
I enjoyed the course, but the readings were too long and the professor was mean.
"""

TEST_TEXT_2 = """
This is a text that does not contain any target aspects.
"""

TEST_TEXT_3 = """
The class was good. I liked the course.
"""

TEST_TEXT_4 = (
    "Professor Doe was a very passionate lecturer who presented "
    "the material quite differently from other courses I have taken. The "
    "only 'problem' I had with his course was how much bias and personal "
    "opinion they interjected in their lectures. A lot of the material "
    "presented was really just opinion and we spent too much time on that, "
    "which did not effectively facilitate learning of the subject matter. "
    "The extra material they brought in, however, was quite interesting and "
    "helped provide deeper understanding of certain subjects."
)

TEST_TEXT_5 = "The mid-terms were horrible. I wish the mid term was less boring."

TEST_TEXT_6 = "Professor Doe was a great instructor."


@pytest.fixture
def doc1():
    doc1 = asp.make_doc(TEST_TEXT_1, aspects=ASPECTS_1, parent_span_min_length=0)
    return doc1


@pytest.fixture
def doc2():
    doc2 = asp.make_doc(TEST_TEXT_2, aspects=ASPECTS_1, parent_span_min_length=0)
    return doc2


@pytest.fixture
def doc3():
    doc3 = asp.make_doc(TEST_TEXT_3, aspects=ASPECTS_1)
    return doc3


@pytest.fixture
def doc4():
    aspects = {
        "course": ["course"],
        "format": ["format"],
        "content": ["content"],
        "professor": ["professor"],
    }
    doc4 = asp.make_doc(TEST_TEXT_4, aspects=aspects)
    return doc4


@pytest.fixture
def doc5():
    aspects = {"tests": ["mid-term", "mid term"]}
    doc5 = asp.make_doc(TEST_TEXT_5, aspects=aspects)
    return doc5

@pytest.fixture
def doc6():
    doc6 = asp.make_doc(TEST_TEXT_6, anonymize=True)
    return doc6


def test_function_make_doc(doc1, doc3):
    """Tests that the make_doc() function returns a spacy Doc object."""
    assertion1 = "Should be a spacy Doc object"
    assert isinstance(doc1, Doc), assertion1

    assertion2 = "Should have a length of 19"
    assert len(doc1) == 19, assertion2

    assert isinstance(doc3, Doc)


def test_attribute_contains_aspect(doc1, doc2):
    """Tests that docs are assigned the contains_aspect attribute as expected."""
    assertion1 = "doc1 should return True"
    assert doc1._.contains_aspect == True, assertion1

    assertion2 = "doc2 should return False"
    assert doc2._.contains_aspect == False, assertion2


def test_attribute_aspects(doc1, doc2):
    """Tests that docs are assigned the aspects attribute as expected."""
    assertion1 = "doc1 should contain 'course', 'content', and 'instructor'"
    doc1_aspects = ["course", "content", "instructor"]
    assert doc1._.aspects == doc1_aspects, assertion1

    assertion2 = "doc2 should contain None"
    doc2_aspects = None
    assert doc2._.aspects == doc2_aspects, assertion2


def test_attribute_keywords(doc1, doc2):
    """Tests that docs are assigned the keywords attribute as expected."""
    assertion1 = "doc1 should contain keyword %s"
    doc1_targets = ["course", "reading", "professor"]
    doc1_keywords = [kw.lemma_.lower() for kw in doc1._.keywords]
    for target in doc1_targets:
        assert target in doc1_keywords, assertion1 % target

    assertion2 = "doc2 should contain no keywords"
    doc2_targets = None
    assert doc2._.keywords == doc2_targets, assertion2


def test_attribute_keyword_aspects(doc1):
    """Tests that tokens are assigned the aspect attribute as expected."""
    assertion = "%s aspect should be %s"
    target_aspects = ["course", "content", "instructor"]
    for keyword, aspect in zip(doc1._.keywords, target_aspects):
        assert keyword._.aspect == aspect, assertion % (keyword.text, aspect)


def test_attribute_parent_span(doc1, doc2):
    """Tests that tokens are assigned the parent span attribute as expected."""
    assertion1 = "Span should read 'the professor was mean'"
    doc1_target = "the professor was mean"
    token1 = doc1._.keywords[2]
    assert token1._.parent_span.text == doc1_target, assertion1

    assertion2 = "Span should be None"
    doc2_target = None
    token2 = doc2[-3]
    assert token2._.parent_span == doc2_target, assertion2


def test_attribute_parent_span_length(doc4):
    """Tests that token parent spans are above minimum length."""
    kw = doc4._.keywords[0]
    span = kw._.parent_span
    target = (
        "Professor Doe was a very passionate lecturer who presented the "
        "material quite differently from other courses I have taken."
    )
    assertion = f"Span should read {target}"

    assert span.text == target, assertion


def test_attribute_parent_span_sentiment(doc1):
    """Tests that spans are assigned sentiment attribute as expected."""
    assertion = "course parent span sentiment should be 0.2846"
    span = doc1._.keywords[0]._.parent_span
    target_sentiment = 0.2846

    assert span._.sentiment == target_sentiment, assertion


def test_attribute_aspect_sentiments(doc1, doc3):
    """Tests that docs are assigned aspect sentiments attribute as expected."""
    target_sentiments1 = {
        "course": 0.2846,
        "content": 0,
        "assignments": None,
        "tests": None,
        "instructor": 0,
    }
    assertion1 = f"Sentiment dict should look like: {target_sentiments1}"

    assert doc1._.aspect_sentiments == target_sentiments1, assertion1

    target_course_sentiment = 0.43095
    course_sentiment = doc3._.aspect_sentiments["course"]

    assertion2 = "doc3 course sentiment value should within 0.00001 of 0.43095"

    assert abs(target_course_sentiment - course_sentiment) <= 0.00001, assertion2


def test_make_doc_with_aspects_from_file():
    """Tests that make_doc() function is able to accept aspects from file path."""
    assertion = "Should successfully take aspects from a file path"
    aspects = ASPECTS_1_PATH
    doc = asp.make_doc(TEST_TEXT_1, aspects=aspects)

    assert doc._.aspect_sentiments is not None, assertion


def test_make_doc_error_from_non_path_aspects_string():
    """Tests that make_doc() function returns ValueError for non-path strings."""
    assertion = "Should raise a ValueError for passing a non-path string to aspects"
    aspects = "This is a string that should raise an error"
    with pytest.raises(ValueError) as excinfo:
        target_error = "Aspects must be either a dict or path to .toml file"
        asp.make_doc(TEST_TEXT_1, aspects=aspects)
        assert excinfo.value == target_error, assertion


def test_multi_word_expression_keywords(doc5):
    """Tests that multi-word expressions in aspect keywords are not split by tokenizer"""
    target_len = 13
    assertion1 = f"Length of doc should be {target_len} tokens"
    assert len(doc5) == target_len, assertion1

    target_kws = ["mid-term", "mid term"]
    kws = [kw.lemma_ for kw in doc5._.keywords]
    assertion2 = f"Keywords in doc should {target_kws}"
    assert kws == target_kws, assertion2

def test_anonymized(doc6):
    """Tests that text is being anonymized as intended"""
    target = "Professor *** was a great instructor."
    assertion = f"anonymized attribute should be {target}."
    assert doc6._.anonymized == target, assertion
