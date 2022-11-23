import os
import tomllib

FILE_DIR = os.path.dirname(__file__)
PROJECT_DIR = os.path.dirname(FILE_DIR)
DATA_DIR = os.path.join(FILE_DIR, 'data')
ASPECT_FILE = os.path.join(DATA_DIR, 'aspects.toml')

def get_aspects_from_file(
    file_path: str,
) -> dict:
    """Gets dictionary of aspects from .toml aspects file.

    Args:
        file_path (str): Path to aspects file. Must be a .toml file in the shape
            described in documentation.

    Returns:
        dict: Dictionary of aspects and corresponding keywords.
    """
    with open(file_path, 'rb') as file:
        aspects = tomllib.load(file)
    return aspects

def get_keywords_from_aspects(
    aspects: dict,
) -> list:
    """Extracts list of keywords from dictionary of aspects.

    Args:
        aspects (dict): Dictionary of aspects and corresponding keywords.

    Returns:
        list: List of all keywords contained in aspects dict.
    """
    keywords = []
    for keywords_list in aspects.values():
        keywords.extend(keywords_list)
    return keywords

def get_default_aspects() -> dict:
    """Retrieves dictionary of default aspects in la_nlp/data/aspects.toml.

    Returns:
        dict: Dictionary of aspects and corresponding keywords.
    """
    return get_aspects_from_file(ASPECT_FILE)
