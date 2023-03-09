import numpy as np
import pandas as pd
from pathlib import Path
from colorama import Fore, Style
from dateutil.parser import parse
from research_pulse.params import *
from research_pulse.logic import search

def load_data_main():
    """
    Load the dataset from the processed folder
    """
    data = pd.read_csv('~/deepdipper/data/processed/aiml_arxiv_with_cit.csv', low_memory=False)
    return data

def launch_search(query):
    data=search.data()
    vector, matrix = search.vectorizer(data)
    results=search.search(query=query, vector=vector, matrix=matrix)
    return results

def vectorizer_main(data):
    """
    vectorize abstracts, and return tfidf_vectorizer and tfidf_matrix to reusage
    """
    return search.vectorizer(data)

vector, matrix = vectorizer_main(load_data_main())

def search_main(query, vector, matrix):
    """
    calls the search function from logic/search.py and returns the top 5 results in list of str format.
    """
    return search.search(query=query, vector=vector, matrix=matrix)

if __name__ == '__main__':
    import sys
    args = sys.argv
    globals()[args[1]](*args[2:])
