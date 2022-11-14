# LA NLP

This package contains code for various natural language processing (NLP) tasks for the UBC Arts ISIT Learning Analytics team.

## Installation

Run the following command to install the package:

```
pip install la_nlp --index-url \
https://<token_name>:<token>@repo.code.ubc.ca/api/v4/projects/879/packages/pypi/simple
```

Where `<token_name>` can be substituted with your personal access token from GitLab, and `<token>` is the token itself. If you have not set up your personal access tokens, please look at the readme file on our package registry [here](https://repo.code.ubc.ca/arts-isit/la-team/pypi_packages).

### Language model

You will also need to install the `spacy` language model used in the package. To do, run the following command:

```
python -m spacy download en_core_web_lg
```

## Usage

As of the current version, the primary way to use this package is with the contained `spacy` pipelines, contained in this `pipes` directory. Typical usage looks something like this:

```
from la_nlp.pipes import aspect_sentiment as asp

text = "Some text"

doc = asp.make_doc(text)
```

The resulting `doc` object should then contain all attributes created with the selected pipeline. For details about which attributes each pipeline generates, see the pipeline's corresponding file in `docs`.