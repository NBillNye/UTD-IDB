#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

from frontend.MLModel import keyword_extraction

class Doc:
    def __init__(self, text: str, keywords: list, origin: str | int):
        self.text = text # full text of one theme
        self.keywords = keywords # words that highlight the document's theme
        self.origin = origin # any course material: str | thread ID: int
        
    def __init__(self):
        return
        
    def set_text(self, text: str):
        self.text = text
    
    def set_keywords(self, keywords: list):
        self.keywords = keywords
        
    def set_origin(self, origin: str | int):
        self.origin = origin
        if type(origin) is str:
            self.type = 'file'
        else:
            self.type =  'thread'

# getter and setter for inputs
class Inputs:
    def __init__(self, class_ID: int , query: str):
        self.class_ID = class_ID
        self.query = query

    def __init__(self):
        return

    def set_class_ID(self, class_ID):
        self.class_ID = class_ID

    def set_query(self, query):
        self.query = query
        
    def get_query_keywords(self):
        kw_model = keyword_extraction.load()
        
        return keyword_extraction.extract_keywords(kw_model, self.query, ngram_range=2, top_n=3) #TENTATIVE ARGS

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Website.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
