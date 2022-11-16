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

### Importing

This module can be imported using the following code:

```
from la_nlp.pipes import aspect_sentiment as asp
```

### `asp.make_doc(text)`

Generates a `spacy` `Doc` object from the input text via the `aspect_sentiment` NLP pipeline.

**Parameters**

`text` (*str*) -- The text to generate a `Doc` from.
<br>
`aspects` (*dict*, optional) -- A dictionary of aspects and corresponding keywords to use for analysis of the input text. If no argument is passed, the module will use the default aspects in  `la_nlp/data/aspects.toml`. Should take following form:

```
{
    'aspect1': ['keyword1', 'keyword2', 'keyword3'],
    'aspect2': ['keyword4', 'keyword5'],
}
```
In the above case, the text will be searched for all references to 'keyword4' and 'keyword5', and map their sentiments to the 'aspect2'.
<br>
`parent_span_min_length` (*int*, optional) -- The minimum length for parent spans upon which sentiment scores will be calculated. Sometimes the model evaluates the parent span of a word to be exceptionally short (sometimes only 'the *aspect*') which is obviously not very useful. This parameter allows you to set a minimum length for these spans. Defaults to 7.

**Returns**

`doc` -- A `spacy` `Doc` object with the following custom attributes assigned for ABSA:

* `Doc._.contains_aspect` (*bool*) -- True if `Doc` contains any of the keywords passed with the `aspects` parameter. False if none were found.
* `Doc._.aspects` (*list*) -- A list of all aspects found within the text.
* `Doc._.keywords` (*list*) -- A list of `spacy` `Token` objects whose lemma correspond to the keywords passed via the `aspects` parameter.
* `Token._.aspect` (*str*) -- The corresponding aspect for each keyword found in the text. This attribute is assigned to all `Token` objects, but will return `None` for all non-keyword tokens.
* `Token._.parent_span` (*Span*) -- A `spacy` `Span` object with the segment of the text that contains the token. This attribute is assigned to all `Token` objects, but will return `None` for all non-keyword tokens due to performance. This behaviour can be disabled by directly calling the `parent_span()` function in `la_nlp.components`.
* `Span._.sentiment` (*float*) -- The compound sentiment score calculated for the corresponding `Span` object using VADER. This attribute is assigned to all `Span` objects, but will return `None` for all spans that are **not** parent spans of a keyword. This behaviour can be disabled by directly calling the `parent_span_sentiment()` function in `la_nlp.components`.
* `Doc._.aspect_sentiments` (*dict*) -- Returns a dictionary of each aspect passed into the `make_doc()` function with corresponding sentiment scores. Aspects with no keywords found in the text will be assigned a `None` value. Calculation of these scores is done by taking the mean of the sentiments of all keywords corresponding to each aspect.

**Typical usage**

```
from la_nlp.pipes import aspect_sentiment as asp

text = "I enjoyed the course, but the readings were boring."
doc = asp.make_doc(text)

print(doc._.aspect_sentiments)

# output: {'course': 0.2846, 'content': -0.4497, 'assignments': None, 'tests': None, 'instructor': None}
