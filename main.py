#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# Standard libraries
import os
import argparse
import csv
from itertools import chain

# NLP libraries
import nltk
from gensim.models import LdaModel, LdaMulticore, TfidfModel
from gensim import corpora

# local libraries
import utils.misc_preprocessing as mp
import utils.spacy_preprocessing as sp
import utils.nltk_preprocessing as nltk_prep
from extract_fb_msg import extract_fb_msg


def main():

    args = parse_arguments()
    if args.file:
        url = "file://" + os.path.abspath(args.file)
    elif args.multiple_files:
        print("Not yet implemented.")
        for f in args.multiple_files:
            print(f)



    print("Extracting messages ...")
    df = extract_fb_msg(url)
    messages = list(df.message)
    messages = mp.doc_granularity(messages, 10)

    # preprocessing
    print("Preprocessing steps ...")

    filename_stopwords = "stopwords_additional.csv"
    try:
        with open(filename_stopwords, 'r') as f:
            content = csv.reader(f)
            additional_stopwords = [word for word in content]
    except FileNotFoundError as e:
        print(e)
        additional_stopwords = []

    stop_words = nltk_prep.get_stopwords('french', additional_stopwords)
    special_char = r"'’*-"
    re_expr = r'[^A-z ]+'

    messages = mp.remove_accent(messages)
    messages = mp.replace_special_character(messages, special_char)
    messages = mp.re_sub_documents(messages, re_expr)
    messages = mp.remove_large_space(messages)


    tok_normalization = "lemma"
    if tok_normalization == "lemma":
        # lemmatization
        print("Lemmatization ...")
        messages = sp.lemmatize(messages)
        messages_split = nltk_prep.doc2tok(messages)
    elif tok_normalization == "stem":

        # tokenization
        print("Tokenization ...")
        #messages_split = nltk_prep.doc2tok(messages_lemma)
        messages_split = nltk_prep.doc2tok(messages)

        # stemming
        messages_split = nltk_prep.stemmize(messages_split)

    # preprocessing after tokenization
    print("Post tokenization ...")
    messages_split = mp.tolower(messages_split)
    messages_split = nltk_prep.remove_stopwords(messages_split, stop_words)
    messages_split = mp.remove_empty(messages_split)

    # Statistics on corpus
    messages_full = list(chain(*messages_split))
    fdist = nltk.FreqDist(messages_full)
    #fdist.plot(100, cumulative=True)
    common_words = [w[0] for w in fdist.most_common(300)]
    hapaxes = fdist.hapaxes()
    messages_split = nltk_prep.remove_stopwords(messages_split, common_words)
    messages_split = nltk_prep.remove_stopwords(messages_split, hapaxes)


    print("Building dictionary ...")
    dictionary = corpora.Dictionary(messages_split)
    corpus = [dictionary.doc2bow(line) for line in messages_split]

    print("Topic extraction with LDA.")
    n_topics = 10
    print("Number of topics: " +str(n_topics))
    lda_model = LdaMulticore(corpus=corpus,
                            id2word=dictionary,
                            num_topics= n_topics,
                            passes=10)

    topics = [[dictionary[elt[0]] for elt in lda_model.get_topic_terms(topic_id)] \
             for topic_id in range(n_topics)]
    print("Printing topics:")
    [print(t) for t in topics]


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Extract topics from facebook message file."
    )

    parser.add_argument(
        "file",
        nargs="?",
        type=str,
        help="Either relative or absolute path for the html file.",
    )
    parser.add_argument(
        "-f",
        "--file_name",
        type=str,
        help="Either relative or absolute path for the html file.",
    )
    parser.add_argument(
        "-ff",
        "--multiple_files",
        nargs='+',
        type=str,
        help="Either relative or absolute paths for the html files.",
    )

    return parser.parse_args()


if __name__ == "__main__":
    main()
