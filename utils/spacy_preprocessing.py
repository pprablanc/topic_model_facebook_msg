#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 15:17:50 2019

@author: pierre
"""

import spacy
import os
#from spacy_lefff import LefffLemmatizer, POSTagger     # Doesn't seem to work anymore

def lemmatize(documents, language = "french"):

    try:
        print("Loading fr_core_news_sm from spacy ...")
        nlp = spacy.load('fr_core_news_sm')
    except IOError as e:
        print(e)
        print("Downloading fr_core_news_sm from spacy ...")
        os.system("python -m spacy download fr_core_news_sm")
        print("Loading fr_core_news_sm from spacy ...")
        nlp = spacy.load('fr_core_news_sm')

    documents_lemma_split = [[tok.lemma_ for tok in nlp(doc)] for doc in documents]
    documents_lemma = [" ".join(m_split) for m_split in documents_lemma_split]
    return documents_lemma
