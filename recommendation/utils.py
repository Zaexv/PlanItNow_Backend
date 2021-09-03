"""De momento este utils va a ser una forma de probar scripts. Ya lo cambiaré más adelanteG"""

from deep_translator import GoogleTranslator

from plans.models import Plan
### PLN ###

import requests
import numpy as np
import emoji
import regex
import string
import nltk
from collections import Counter

from nltk.corpus import stopwords
from nltk.corpus import words
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet as wn




def translateAllPlans():
    for plan in Plan.objects.all():
        print("\t Traduciendo plan...{plan.id}")
        english_title = GoogleTranslator(source='auto', target='en').translate(text=plan.title)
        print(english_title)

        english_description = GoogleTranslator(
            source='auto', target='en').translate(text=plan.description)
        print(english_description)

        plan.english_title = english_title
        plan.english_description = english_description
        plan.save()


def get_lemmas(text):
    '''
    Lematiza el texto con la libreria nlp
    '''

    custom_stopwords = [
        'hi', '\n', '\n\n', '&amp;', ' ',
        '.', '-', 'got', "it's", 'it’s',
        "i'm", 'i’m', 'im', 'want', 'like',
        '$', '@', ' !', ' ?', '#', "''", '``',
        "n't", "'m", "'s", ':', '...', '!', '?', ',',
        'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
        'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
        'thanks', 'let'
    ]


    text = text.lower()
    english_words = words.words()
    all_words = word_tokenize(text)

    is_noun = lambda pos: pos[:2] == 'NN'
    is_verb = lambda pos: pos[:2] == 'VBP' #| pos[:2] == 'VB'
    nouns = [word for (word, pos) in nltk.pos_tag(all_words) if (is_noun(pos) | is_verb(pos))]

    text_without_stop = ''

    for word in nouns:
        word = word.lower()
        is_english_word = (word not in custom_stopwords) and (word in english_words)
        if (is_english_word):
            text_without_stop = text_without_stop + word + ' '

    words_without_stop = word_tokenize(text_without_stop);

    lemmatizer = WordNetLemmatizer()

    lemmas = words_lemma = [lemmatizer.lemmatize(word) for word in words_without_stop]

    return lemmas