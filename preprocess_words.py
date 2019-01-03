#!/usr/bin/python
import nltk
from nltk import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import LancasterStemmer, WordNetLemmatizer
import re, string, unicodedata, contractions, inflect
from bs4 import BeautifulSoup

import sqlite3
import sys
import csv

def denoise_text(text):
    # remove text between brackets
    text = re.sub('\[[^]]*\]', '', text)
    # Replace contractions in string of text
    text = contractions.fix(text)
    return text

# Convert all characters to lowercase from list of tokenized words
def to_lowercase(words):
    new_words = []
    for word in words:
        new_word = word.lower()
        new_words.append(new_word)
    return new_words

# Remove punctuation from list of tokenized words
def remove_punctuation(words):
    new_words = []
    for word in words:
        new_word = re.sub(r'[^\w\s]', '', word)
        if new_word != '':
            new_words.append(new_word)
    return new_words

# Replace all integers
def replace_numbers(words):
    p = inflect.engine()
    new_words = []
    for word in words:
        if not word.isdigit():
            new_words.append(word)
    return new_words

# Remove stop words from list of tokenized words
def remove_stopwords(words):
    new_words = []
    for word in words:
        if word not in stopwords.words('english'):
            new_words.append(word)
    return new_words

# use above methods to normalize text
def normalize(words):
    words = to_lowercase(words)
    words = remove_punctuation(words)
    words = replace_numbers(words)
    words = remove_stopwords(words)
    return words

# Lemmatize verbs in list of tokenized words
def lemmatize_verbs(words):
    lemmatizer = WordNetLemmatizer()
    lemmas = []
    for word in words:
        lemma = lemmatizer.lemmatize(word, pos='v')
        lemmas.append(lemma)
    return lemmas

# Connect to created database 
con = sqlite3.connect('news.db')

cur = con.cursor()
cur.execute("SELECT COUNT(*) FROM BBCnews;")
num_rows = cur.fetchone()[0]

# Preform preprocessing on article text for each article in the database
for row in range(num_rows):
    cur.execute("SELECT Article FROM BBCnews WHERE ID = ?;", (row + 1,))
    text = cur.fetchone()[0]
    text = denoise_text(text)
    words = nltk.word_tokenize(text) # tokenize the text into a list of the words
    words = normalize(words)
    words = lemmatize_verbs(words)
    string_words = ", ".join(words)
    # add string of the words into the table
    cur.execute("UPDATE BBCnews SET Words = ? WHERE ID = ?;", (string_words, row + 1,))
    
con.commit()
con.close()

