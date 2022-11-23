import os
from la_nlp import utils

FILE_DIR = os.path.dirname(__file__)

ASPECTS_1 = os.path.join(FILE_DIR, 'test_data', 'test_aspects_1.toml')
ASPECTS_2 = os.path.join(FILE_DIR, 'test_data', 'test_aspects_2.toml')

def test_get_aspects_from_file():
    aspects = utils.get_aspects_from_file(ASPECTS_1)
    target = {
        'course':['course','class','lecture'],
        'content':['content','material','reading','syllabus','powerpoint'],
        'assignments':['assignment','project','paper','homework'],
        'tests':['test','quiz','exam','examination','midterm',
                 'mid-term','final'],
        'instructor':['instructor','teacher','professor','prof','dr']
    }
    assertion = f'Aspects should be {aspects}.'
    assert aspects == target, assertion

def test_keywords_from_aspects():
    aspects = utils.get_aspects_from_file(ASPECTS_1)
    keywords = utils.get_keywords_from_aspects(aspects)
    target = ['course','class','lecture','content','material','reading',
              'syllabus','powerpoint','assignment','project','paper','homework',
              'test','quiz','exam','examination','midterm','mid-term','final',
              'instructor','teacher','professor','prof','dr']
    assertion = f'Keywords should be {target}.'
    assert keywords == target, assertion
