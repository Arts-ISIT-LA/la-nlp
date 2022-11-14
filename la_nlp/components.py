from la_nlp import config
from spacy.tokens import Doc, Span, Token
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Initializing the VADER sentiment analyzer for use within sentiment components
ANALYZER = SentimentIntensityAnalyzer()

def set_extension(
    extension_name: str,
    default_val: any = None,
    target_obj: Doc | Span | Token = Doc,
) -> None:
    """Sets an extension on a designated spacy object if doesn't already exist.

    Args:
        extension_name (str): Name of the extension/attribute to be set.
        default_val (any, optional): Default value for all objects with
            the extension to be initialized to. Defaults to None.
        target_obj (Doc | Span | Token, optional): The spacy object onto which
            the extension should be set. Defaults to Doc.
    """
    if not target_obj.has_extension(extension_name):
        target_obj.set_extension(extension_name, default=default_val)

def contains_aspect(
    doc: Doc,
    base_keywords: list,
) -> Doc:
    """Takes a Doc and returns a new Doc with the 'contains_aspect' attribute.

    Accessed via 'Doc._.contains_aspect', the 'contains_aspect' attribute is a
    boolean which indicates whether or not doc contains any of the keywords
    passed to function.

    Target object: spacy Doc
    Attribute type: bool
    Default value: False
    Dependent on: N/A

    Args:
        doc (Doc): The Doc object to set the attribute on.
        base_keywords (list): List of keywords to search for within the Doc.

    Returns:
        Doc: Processed Doc object with the 'contains_aspect' attribute.
    """
    set_extension('contains_aspect', default_val=False)
    
    for token in doc:
        if token.lemma_.lower() in base_keywords:
            doc._.contains_aspect = True
            break
    
    return doc

def aspects(
    doc: Doc,
    base_aspects: dict,
) -> Doc:
    """Takes a Doc and returns a new Doc with the 'aspects' attribute.

    Accessed via 'Doc._.aspects', the 'aspects' attribute contains a list of the
    aspects discussed by the Doc.

    Target object: spacy Doc
    Attribute type: list
    Default value: None
    Dependent on: Doc._.contains_aspect

    Args:
        doc (Doc): The Doc object to set the attribute on.
        base_aspects (dict): Dictionary of keywords mapped to aspects. Should
            take the form of: {'aspect1': ['keyword1', 'keyword2'], 'aspect2':
            ['keyword3', 'keyword4']}.

    Returns:
        Doc: Processed Doc object with the 'aspects' attribute.
    """
    set_extension('aspects')
    
    if doc._.contains_aspect == True:
        aspects_contained = []
        for token in doc:
            for aspect in base_aspects:
                if aspect in aspects_contained:
                    continue
                keywords = base_aspects[aspect]
                if token.lemma_.lower() in keywords:
                    aspects_contained.append(aspect)
        doc._.aspects = aspects_contained
    return doc

def keywords(
    doc: Doc,
    base_keywords: list,
) -> Doc:
    """Takes a Doc and returns a new Doc with the 'keywords' aspect.

    Accessed via 'Doc._.keywords', the 'keywords' attribute contains a list of
    the keywords contained within the Doc.

    Target object: spacy Doc
    Attribute type: list
    Default value: None
    Dependent on: Doc._.contains_aspect

    Args:
        doc (Doc): The Doc object to set the attribute on.
        base_keywords (list): List of keywords to search for within the Doc.

    Returns:
        Doc: Processed Doc object with the 'keywords' attribute.
    """
    set_extension('keywords')

    if doc._.contains_aspect == True:
        keywords = []
        for token in doc:
            if token.lemma_.lower() in base_keywords:
                keywords.append(token)
        doc._.keywords = keywords
    return doc

def keyword_aspects(
    doc: Doc,
    base_aspects: dict,
) -> Doc:
    """Takes a Doc and adds the 'aspect' attribute to its Token objects.

    Accessed via 'Token._.aspect', the 'aspect' attribute is applied only to the
    Token objects contained within the 'keywords' attribute of the Doc. The
    attribute itself reflects the corresponding aspect of the keyword. Non-
    keyword Token objects receive a None value.

    Target object: spacy Token
    Attribute type: string
    Default value: None
    Dependent on: Doc._.keywords

    Args:
        doc (Doc): The Doc object for whose Token objects to set the attribute
            on.
        base_aspects (dict): Dictionary of keywords mapped to aspects. Should
            take the form of: {'aspect1': ['keyword1', 'keyword2'], 'aspect2':
            ['keyword3', 'keyword4']}.

    Returns:
        Doc: Processed Doc object with Token objects containing the 'aspect'
            attribute.
    """
    set_extension('aspect', target_obj=Token)

    if doc._.keywords == None:
        return doc

    for doc_keyword in doc._.keywords:
        for aspect in base_aspects:
            for keyword in base_aspects[aspect]:
                if doc_keyword.lemma_.lower() == keyword:
                    doc_keyword._.aspect = aspect
                continue
            if doc_keyword._.aspect != None:
                continue
        if doc_keyword._.aspect != None:
            continue

    return doc

def parent_span(
    doc: Doc,
    include_non_keywords: bool = False,
) -> Doc:
    set_extension('parent_span', target_obj=Token)

    if include_non_keywords == True:
        tokens = doc
    elif include_non_keywords == False and doc._.keywords is not None:
        tokens = doc._.keywords
    elif include_non_keywords == False and doc._.keywords is None:
        return doc
    else:
        raise ValueError('include_non_keywords takes only True or False')

    for token in tokens:
        head = token.head
        siblings = head.children
        indices = [token.i for token in siblings]
        indices.append(head.i)
        indices.sort()
        first = indices[0]
        last = indices[-1] + 1
        if last >= len(doc):
            span = doc[first:]
        else:
            span = doc[first:last]
        token._.parent_span = span          

    return doc

def parent_span_sentiment(doc, include_non_keywords=False):
    set_extension('sentiment', target_obj=Span)

    if include_non_keywords == True:
        tokens = doc
    else:
        tokens = doc._.keywords
    
    if tokens == None:
        return doc
    
    for token in tokens:
        scores = ANALYZER.polarity_scores(token._.parent_span.text)
        sentiment = scores['compound']
        token._.parent_span._.sentiment = sentiment
    
    return doc

def aspect_sentiments(doc, base_aspects):
    set_extension('aspect_sentiments')

    aspect_sentiments = {aspect:None for aspect in base_aspects}

    if doc._.keywords != None:
        for keyword in doc._.keywords:
            aspect = keyword._.aspect
            sentiment = keyword._.parent_span._.sentiment
            aspect_sentiments[aspect] = sentiment
    
    doc._.aspect_sentiments = aspect_sentiments

    return doc
