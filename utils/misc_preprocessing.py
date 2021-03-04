#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unicodedata
import re

def strip_accents(s):
   return ''.join(c for c in unicodedata.normalize('NFD', s)
                  if unicodedata.category(c) != 'Mn')
   
def remove_accent(documents):
    new_documents = [strip_accents(doc) for doc in documents]
    return new_documents

def remove_large_space(documents):
    new_documents = [re.sub(r' +', ' ', doc) for doc in documents]
    return new_documents

def remove_empty(documents_splits):
    new_documents = [[m for m in doc_split if m] for doc_split in documents_splits if doc_split]
    return new_documents

def replace_special_character(documents, special_char, replace_by = " "):
    new_documents = [re.sub('['+special_char+']', replace_by, doc) for doc in documents]
    return new_documents

def re_sub_documents(documents, re_expr, replace_by = " "):
    new_documents = [re.sub(re_expr, replace_by, doc) for doc in documents]
    return new_documents

def tolower(documents_split):
    new_documents = [[m.lower() for m in doc_split] for doc_split in documents_split]
    return new_documents

def doc_granularity(documents, granularity = 2):
    new_dococuments = [" ".join(documents[i:i+granularity]) for i in range(0, len(documents), granularity)]
    return new_dococuments
