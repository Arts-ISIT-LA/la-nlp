import tomllib
import os

FILE_DIR = os.path.dirname(__file__)
PROJECT_DIR = os.path.dirname(FILE_DIR)
DATA_DIR = os.path.join(PROJECT_DIR, 'data')
ASPECT_FILE = os.path.join(DATA_DIR, 'aspects.toml')

def get_aspects(file_path=ASPECT_FILE):
    with open(file_path, 'rb') as file:
        aspects = tomllib.load(file)
    return aspects
