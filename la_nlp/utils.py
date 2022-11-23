import tomllib
import os

FILE_DIR = os.path.dirname(__file__)
PROJECT_DIR = os.path.dirname(FILE_DIR)
DATA_DIR = os.path.join(FILE_DIR, 'data')
ASPECT_FILE = os.path.join(DATA_DIR, 'aspects.toml')

def get_aspects_from_file(file_path=ASPECT_FILE):
    with open(file_path, 'rb') as file:
        aspects = tomllib.load(file)
    return aspects

def get_keywords_from_aspects(aspects):
    keywords = []
    for keywords_list in aspects.values():
        keywords.extend(keywords_list)
    return keywords