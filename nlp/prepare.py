import unicodedata
import re
import json

import nltk
from nltk.tokenize.toktok import ToktokTokenizer
from nltk.corpus import stopwords

import pandas as pd

import acquire

list_of_blog = acquire.get_blog_articles()
list_of_news = acquire.get_news_articles()

extra_words = ['']
exclude_words = ['']


def basic_clean(article):
    article = re.sub(r'\s', ' ', article).lower()
    article = unicodedata.normalize('NFKD', article)\
        .encode('ascii', 'ignore')\
        .decode('utf-8', 'ignore')
    article = re.sub(r"[^a-z0-9'\s]", '', article)
    return article


def tokenize(article):
    tokenizer = nltk.tokenize.ToktokTokenizer()
    article = tokenizer.tokenize(article, return_str=True)
    return article
    

def stem(article):
    ps = nltk.porter.PorterStemmer()
    stems = [ps.stem(word) for word in article.split()]
    article_stemmed = ' '.join(stems)
    return article_stemmed


def lemmatize(article):
    wnl = nltk.stem.WordNetLemmatizer()
    lemmas = [wnl.lemmatize(word) for word in article.split()]
    article_lemmatized = ' '.join(lemmas)
    return article_lemmatized


def remove_stopwords(article, extra_words = [], exclude_words = []):
    stopword_list = stopwords.words('english')
    [stopword_list.append(word) for word in extra_words if word not in stopword_list]
    [stopword_list.remove(word) for word in exclude_words if word in stopword_list]
    words = article.lower().split()
    filtered_words = [w for w in words if w not in stopword_list]
    article_without_stopwords = ' '.join(filtered_words)
    return article_without_stopwords


def prep_article(dictionary_article, extra_words = [], exclude_words = []):
    if 'category' in dictionary_article:
        cleaned_dict = {
        'title': dictionary_article['title'],
        'category': dictionary_article['category'],
        'original': dictionary_article['content'],
        'stemmed': stem(dictionary_article['content']),
        'lemmatized': lemmatize(dictionary_article['content']),
        'clean': remove_stopwords(basic_clean(dictionary_article['content']), extra_words, exclude_words),
            }
        
    else:
        cleaned_dict = {
        'title': dictionary_article['title'],
        'original': dictionary_article['content'],
        'stemmed': stem(dictionary_article['content']),
        'lemmatized': lemmatize(dictionary_article['content']),
        'clean': remove_stopwords(basic_clean(dictionary_article['content']), extra_words, exclude_words),
            }

    return cleaned_dict

def prepare_article_data(dictionary_article, extra_words = [], exclude_words = []):
    clean_dict_list = []
    
    for artical in dictionary_article:
        clean_dict_list.append(prep_article(artical, extra_words, exclude_words))
        
    return clean_dict_list
        