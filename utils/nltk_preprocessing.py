#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import nltk
from nltk.tokenize import word_tokenize 
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from nltk.stem import WordNetLemmatizer

def get_stopwords(language, add_stopwords = []):
    try: 
        stop_words = stopwords.words(language)
    except LookupError:
        nltk.download('stopwords')
        stop_words = stopwords.words(language)
    stop_words = stop_words + add_stopwords
    return stop_words

def remove_stopwords(documents_split, stopwords):
    new_documents_split = [[m for m in doc_split if m not in stopwords] for doc_split in documents_split]
    return new_documents_split

def doc2tok(documents):
    documents_split = [word_tokenize(doc) for doc in documents]
    return documents_split


def stemmize(documents_split, language = "french"):
    stemmer = SnowballStemmer("french")
    documents_split_stem = [[stemmer.stem(m) for m in m_split] for m_split in documents_split]
    return documents_split_stem



