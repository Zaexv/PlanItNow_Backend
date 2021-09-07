"""De momento este utils va a ser una forma de probar scripts. Ya lo cambiaré más adelanteG"""

from deep_translator import GoogleTranslator
from deep_translator.exceptions import NotValidPayload

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




def translate_all_plans():
    for plan in Plan.objects.all():
        print("\t Traduciendo plan...{plan}")
        try:
            english_title = GoogleTranslator(source='auto', target='en').translate(text=plan.title+"")
            english_description = GoogleTranslator(
                source='auto', target='en').translate(text=plan.description)
            print(english_description)
        except NotValidPayload:
            english_title='Not valid'
            english_description='Not valid'
        print(english_title)



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
        'thanks', 'let' , 'ta'
    ]
    text = text.lower()
    english_words = words.words()
    all_words = word_tokenize(text)

    is_noun = lambda pos: pos[:2] == 'NN'
    is_verb = lambda pos: pos[:2] == 'VB'
    is_verb_p = lambda pos: pos[:2] == 'VBP'
    nouns = [word for (word, pos) in nltk.pos_tag(all_words) if (is_noun(pos) | is_verb(pos) | is_verb_p(pos))]

    text_without_stop = ''

    for word in nouns:
        word = word.lower()
        is_english_word = (word not in custom_stopwords) and (word in english_words)
        if (is_english_word):
            text_without_stop = text_without_stop + word + ' '
    words_without_stop = word_tokenize(text_without_stop);
    lemmatizer = WordNetLemmatizer()
    # Ver cómo lematizar según categoría
    lemmas = words_lemma = [lemmatizer.lemmatize(word) for word in words_without_stop]
    return lemmas

def assign_all_plans_lemmas():
    for plan in Plan.objects.all():
        title_lemmas = get_lemmas(plan.english_title)
        description_lemmas = get_lemmas(plan.english_description)
        print(title_lemmas)
        print(description_lemmas)
        print(plan.title)
        print(plan.description)

def calculate_distance_between_plans(plan1, plan2):
    pass
