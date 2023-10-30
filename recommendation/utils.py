"""De momento este utils va a ser una forma de probar scripts. Ya lo cambiaré más adelanteG"""
from datetime import date

from deep_translator.exceptions import NotValidPayload

### PLN ###


import nltk

from deep_translator import GoogleTranslator

from nltk.corpus import words
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

from plans.models import Plan

### PLN ###
from recommendation.models import Lemma, UserDistance
from userprofiles.models import UserProfile


def translate_all_plans():
    for plan in Plan.objects.all():
        print("\t Traduciendo plan...{plan}")
        try:
            english_title = GoogleTranslator(source='auto', target='en').translate(text=plan.title + "")
            english_description = GoogleTranslator(
                source='auto', target='en').translate(text=plan.description)
            print(english_description)
        except NotValidPayload:
            english_title = 'Not valid'
            english_description = 'Not valid'
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
        'thanks', 'let', 'ta', 'am'
    ]

    text = text.lower()
    english_words = words.words()
    tokenized_words = word_tokenize(text)

    is_noun = lambda pos: pos[:2] == 'NN'
    is_noun_plural = lambda pos: pos[:2] == 'NNS'
    is_verb = lambda pos: pos[:2] == 'VB'
    is_verb_p = lambda pos: pos[:2] == 'VBP'
    tagged_words = [word for (word, pos) in nltk.pos_tag(tokenized_words)
                    if (
                            is_noun(pos) | is_verb(pos) | is_verb_p(pos) | is_noun_plural(pos)
                    )
                    ]

    text_without_stop = ''

    for word in tagged_words:
        if (word not in custom_stopwords):
            text_without_stop = text_without_stop + word + ' '
    words_without_stop = word_tokenize(text_without_stop);
    lemmatizer = WordNetLemmatizer()
    lemmas = [lemmatizer.lemmatize(word) for word in words_without_stop]
    lemmas = [lemma for lemma in lemmas
              if (
                      lemma in english_words
              )
              ]
    return lemmas


# Funciona
def assign_all_plans_lemmas():
    for plan in Plan.objects.all():
        title_lemmas = get_lemmas(plan.english_title)
        description_lemmas = get_lemmas(plan.english_description)
        print(title_lemmas)
        print(description_lemmas)
        print(plan.title)
        print(plan.description)
        for lemma in title_lemmas:
            lemma = Lemma.objects.get_or_create(lemma=lemma)[0]
            lemma.corresponding_plans.add(plan)
        for lemma in description_lemmas:
            lemma = Lemma.objects.get_or_create(lemma=lemma)[0]
            lemma.corresponding_plans.add(plan)


def calculate_all_user_distance():
    today = date.today()
    for user in UserProfile.objects.all():
        for plan in Plan.objects.filter(init_date__gte=today):
            calculate_distance_plan_user(plan=plan, user=user)
    pass


def calculate_all_plan_distance():
    pass


def calculate_distance_between_plans(plan1, plan2):
    pass


def calculate_distance_plan_user(plan, user):
    plans_ids = list(user.participant_user.all().values_list('id', flat=True))
    plans_ids.extend(list(Plan.objects.filter(owner__id=user.user.id).values_list('id', flat=True)))
    user_lemmas = set(Lemma.objects.filter(corresponding_plans__id__in=plans_ids).values_list('lemma', flat=True))
    plan_lemmas = set(plan.lemma_set.values_list('lemma', flat=True))
    intersection_lemmas = plan_lemmas.intersection(user_lemmas)
    user_plan_distance = UserDistance.objects.get_or_create(user=user, plan=plan)[0]
    try:
        user_plan_distance.distance = len(intersection_lemmas) / len(user_lemmas)
    except ZeroDivisionError:
        user_plan_distance.distance = -1

    user_plan_distance.save()
    print(user_plan_distance.distance)
    return user_plan_distance.distance


def fill_recommendations():
    translate_all_plans()
    assign_all_plans_lemmas()
    calculate_all_user_distance()
