# **LA NLP**: **L**earning **A**nalytics **N**atural **L**anguage **P**rocessing

## Overview

LA NLP is a Python package in development at [UBC Arts ISIT](https://isit.arts.ubc.ca/) for the application of natural language processing (NLP) techniques to learning analytics (LA) data.

This package is primarily built on top of [spaCy](https://spacy.io/). spaCy uses a [processing pipeline](https://spacy.io/usage/processing-pipelines) which contains a number of different modular components and allows us to insert our own components into this pipeline. LA NLP relies on this functionality by introducing custom components and combining them into pipelines for specific use cases.

As of March 2023, this package is primarily exploratory in nature and contains only [one pipeline for conducting aspect-based sentiment analysis (ABSA)](./docs/docs.md#la_nlppipesaspect_sentiment). However, we hope to include more features over time if there is interest from the UBC learning analytics community and beyond.

For a history of changes, see our [changelog](./docs/changelog.md) (introduced in version `0.4.1`).

## Installation

LA NLP can be easily installed using the following commands:

```bash
pip install la-nlp
python -m spacy download en_core_web_lg
```

## Usage

As of the current version, the primary way to use this package is with the contained `spacy` pipelines, contained in this `pipes` directory. Typical usage looks something like this:

```Python
from la_nlp.pipes import aspect_sentiment as absa

text = "Some text"

doc = absa.make_doc(text)
```

For detailed usage instructions, see our [documentation](./docs/docs.md)

## Developer documentation

*Coming soon*