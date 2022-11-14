# `la_nlp.pipes`

This file contains documentation for the `la_nlp.pipes` module. `pipes` contains various NLP pipelines written with the `spacy` package.

### Basic usage example

Each pipe contains code that will generate a `spacy` `Doc` object with some custom attributes assigned. Basic usage should look something like this:

```
from la_nlp.pipes import aspect_sentiment as asp

text = "Some text."

doc = asp.make_doc(text)
```

The resulting `Doc` object will contain standard `spacy` attributes along with a number of custom attributes. These attributes are detailed in the pipeline's corresponding section of this document.

## `la_nlp.pipes.aspect_sentiment`

The `aspect_sentiment` pipeline conducts aspect-based sentiment analysis on the text based into it. Aspect-based sentiment analysis is an NLP technique used for determining the sentiment (positivity/negativity) towards various aspects (topics) contained within a text. This technique provides a more accurate picture of the opinions expressed in a text when compared to traditional sentiment analysis, which has many downsides.

### The problem with traditional sentiment analysis

Traditionally, sentiment analysis is done using all words in a given text and computing an overall sentiment score for all of the words combined. This works quite well for very short texts (no longer than one sentence), but tends to break down with longer texts.