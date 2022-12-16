"""NLP pipeline for performing aspect-based sentiment analysis with spacy.

This module contains a pipeline for performing aspect-based sentiment analysis
via the spacy NLP package and the VADER sentiment model. The pipeline can be
called via the make_doc() function, which accepts a string as input and returns
a spacy Doc object containing a number of attributes useful for this type of
analysis. See documentation for a list of attributes assigned by this pipeline.
"""

import os
import re

from la_nlp import components, utils

from spacy import load as load_model
from spacy.language import Language
from spacy.tokens import Doc

DEFAULT_ASPECTS = utils.get_default_aspects()

NLP = load_model("en_core_web_lg")


def make_doc(
    text: str,
    aspects: dict | str = DEFAULT_ASPECTS,
    parent_span_min_length: int = 7,
    anonymize: bool = False,
) -> Doc:
    """Generates a spacy Doc object via the aspect sentiment pipeline.

    Args:
        text (str): The text to process.
        aspects (dict | str, optional): The aspects to use for aspect-based
            sentiment analysis. Can be either a dictionary of aspects with
            corresponding arrays of keywords, or a path to a .toml file
            containing the aspect-keyword mappings. Defaults to default aspects
            at la_nlp/data/aspects.toml.
        parent_span_min_length (int, optional): Minimum length from which to
            generate token parent spans. Defaults to 7.
        anonymize (bool, optional): Indicates whether or not to set the 'anonymized'
            Doc attribute. Defaults to False.

    Raises:
        ValueError: Raised if value passed to aspects is not a file path or
            a dictionary.

    Returns:
        Doc: Processed Doc object from input text containing attributes
            generated by the aspect_sentiment pipeline.
    """

    def except_multi_word_expressions(keywords: list) -> None:
        """Creates exception for multi-word expression keywords to not be tokenized.

        Checks for keywords containing characters used for token splitting. For each
        keyword containing a splitter, adds the keyword and its pluralized form to the
        spacy tokenizer as an exception.
        """
        rules = NLP.tokenizer.rules
        regex = r"[-\s/']"
        for keyword in keywords:
            if keyword in rules:
                continue
            if re.search(regex, keyword):
                rules[keyword] = [{65: keyword}]
                rules[keyword + "s"] = [{65: keyword + "s"}]
        NLP.tokenizer.rules = rules

    if isinstance(aspects, str) and os.path.isfile(aspects):
        aspects = utils.get_aspects_from_file(aspects)
    elif not isinstance(aspects, dict):
        raise ValueError("Aspects must be either a dict or path to .toml file")

    keywords = utils.get_keywords_from_aspects(aspects)
    except_multi_word_expressions(keywords)

    cfg = {
        "aspect_sentiment_pipe": {
            "aspects": aspects,
            "keywords": keywords,
            "parent_span_min_length": parent_span_min_length,
            "anonymize": anonymize,
        }
    }
    return NLP(text, component_cfg=cfg)


@Language.component("aspect_sentiment_pipe")
def aspect_sentiment_pipe(
    doc: Doc,
    aspects: dict,
    keywords: list,
    parent_span_min_length: int = 7,
    anonymize: bool = False,
) -> Doc:
    """Compiles the pipeline components into a single function.

    Should not be called publically. This function is only used as an interface
    between the spacy pipeline and the pipeline components contained within this
    package.
    """
    doc = components.set_doc_contains_aspect(doc, keywords)
    doc = components.set_doc_aspects(doc, aspects)
    doc = components.set_doc_keywords(doc, keywords)
    doc = components.set_token_aspects(doc, aspects)
    doc = components.set_token_parent_span(doc, min_length=parent_span_min_length)
    doc = components.set_span_sentiment(doc)
    doc = components.set_doc_aspect_sentiments(doc, aspects)
    if anonymize == True:
        doc = components.set_anonymized(doc)
    return doc


NLP.add_pipe("aspect_sentiment_pipe")
