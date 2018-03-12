"""
    Docstring module
"""

from Log import *
import Log as Log_file
import gzip
import os
import Functions

# pylint: disable=C0301

Log_file.DEBUG_ACTIVATED = True

# pylint: disable=C0103

Train_Path = "../DATAS/train"
Test_Path = "../DATAS/test"
Dev_Path = "../DATAS/dev"

# Case to study

use_unigram = True
use_bigram = True
use_trigram_centered = True
refine = False

# number of .gz file to consider for learning (out of 1500) (+1500 will act as 1500)
# the higher our n-gram is, the more RAM will be used, so number of learning files will have to be lower if we still want a fast computation

learning_files_to_consider = 10

if learning_files_to_consider < 0 :
    learning_files_to_consider = 1
elif learning_files_to_consider > 1500 :
    learning_files_to_consider = 1500

# since we can't consider trigram without considering bigram or bigram without unigram :

if refine :
    use_trigram_centered = True
if use_trigram_centered :
    use_bigram = True
if use_bigram :
    use_unigram = True

# Learning

dict_lemme_to_words = dict()
dict_bigram_wordlemme_to_words = dict()
dict_trigram_centered_wordlemmelemme_to_words = dict()
dict_trigram_centered_wordlemmeword_to_words = dict()

words_lemmes_list_train = []

# if we don't use unigram, we are in the baseline case where we take lemme for our predicitons (just need to leave empty dictionnaries)
if use_unigram :
    words_lemmes_list_train = Functions.extract_data_from_files(Train_Path, learning_files_to_consider)

Log.debug(" ")
Log.debug("Learning :")

stepsForLogging = len(words_lemmes_list_train)/20
current = 0
currentPercentage = 0

for i in range(0, len(words_lemmes_list_train)):

    if i > current :
        Log.debug('{:>5}'.format(str(currentPercentage)+" %"),1)  
        currentPercentage+=5
        current += stepsForLogging

    word_lemme = words_lemmes_list_train[i]

    word = Functions.is_number(word_lemme[0])
    lemme = Functions.is_number(word_lemme[1])

    if "#end document" in word or "#begin document" in word:
        continue

    # UNIGRAM

    if lemme in dict_lemme_to_words :
        dict_words_to_frequence = dict_lemme_to_words[lemme]
    else:
        dict_words_to_frequence = dict()
        dict_lemme_to_words[lemme] = dict_words_to_frequence

    if word in dict_words_to_frequence :
        dict_words_to_frequence[word] += 1
    else:
        dict_words_to_frequence[word] = 1

    # BIGRAM

    if not use_bigram :
        continue

    if i > 0 :
        previousWord = words_lemmes_list_train[i-1][0]
    else:
        previousWord = "."

    if  Functions.contain_stopword(previousWord):
        continue

    bigram = previousWord+" "+lemme

    if bigram in dict_bigram_wordlemme_to_words :
        dict_words_to_frequence = dict_bigram_wordlemme_to_words[bigram]
    else:
        dict_words_to_frequence = dict()
        dict_bigram_wordlemme_to_words[bigram] = dict_words_to_frequence

    if word in dict_words_to_frequence :
        dict_words_to_frequence[word] += 1
    else:
        dict_words_to_frequence[word] = 1


    # TRIGRAMCENTERED WORD LEMME LEMME

    if not use_trigram_centered:
        continue

    if i >= len(words_lemmes_list_train)-1 :
        continue

    nextLemme = words_lemmes_list_train[i+1][1]

    if  Functions.contain_stopword(nextLemme):
        continue

    trigramCentered = bigram+" "+nextLemme

    if trigramCentered in dict_trigram_centered_wordlemmelemme_to_words :
        dict_words_to_frequence = dict_trigram_centered_wordlemmelemme_to_words[trigramCentered]
    else:
        dict_words_to_frequence = dict()
        dict_trigram_centered_wordlemmelemme_to_words[trigramCentered] = dict_words_to_frequence

    if word in dict_words_to_frequence :
        dict_words_to_frequence[word] += 1
    else:
        dict_words_to_frequence[word] = 1

    
    # TRIGRAMCENTERED WORD LEMME WORD

    if not refine:
        continue

    if i >= len(words_lemmes_list_train)-1 :
        continue

    nextWord = words_lemmes_list_train[i+1][0]

    if  Functions.contain_stopword(nextWord):
        continue

    trigramCenteredWLW = bigram+" "+nextWord

    if trigramCenteredWLW in dict_trigram_centered_wordlemmeword_to_words :
        dict_words_to_frequence = dict_trigram_centered_wordlemmeword_to_words[trigramCenteredWLW]
    else:
        dict_words_to_frequence = dict()
        dict_trigram_centered_wordlemmeword_to_words[trigramCenteredWLW] = dict_words_to_frequence

    if word in dict_words_to_frequence :
        dict_words_to_frequence[word] += 1
    else:
        dict_words_to_frequence[word] = 1

Log.debug(str(100)+" %",1)
Log.debug(" ")
Log.debug("Estimating most frequent words")


# Generating dicitonaries

dictionary_lemme_word = Functions.generate_dictionary_from_frequences(dict_lemme_to_words)
del dict_lemme_to_words

dictionary_bigram_wordlemme_word = Functions.generate_dictionary_from_frequences(dict_bigram_wordlemme_to_words)
del dict_bigram_wordlemme_to_words

dictionary_trigramcentered_wordlemmelemme_word = Functions.generate_dictionary_from_frequences(dict_trigram_centered_wordlemmelemme_to_words)
del dict_trigram_centered_wordlemmelemme_to_words

dictionary_trigramcentered_wordlemmeword_word = Functions.generate_dictionary_from_frequences(dict_trigram_centered_wordlemmeword_to_words)
del dict_trigram_centered_wordlemmeword_to_words

# Testing

Log.debug(" ")
Log.debug("Testing :")

# Read files

#words_list_test, lemmes_list_test = Functions.extract_data_from_files(Test_Path, 20, True)

trigramcenteredFound = 0
bigramFound = 0
unigramFound = 0
monogramFound = 0

previous_word = ""
previous_lemme = ""
previous_prediction = ""

predictions_list = []

words_list_test, lemmes_list_test = Functions.extract_data_from_files(Test_Path, 20, True)

for i in range(0, len(words_list_test)):

    word = words_list_test[i]
    lemme = lemmes_list_test[i]

    bigram = Functions.is_number(previous_prediction)+" "+lemme
    trigramcentered = ""
    if i < len(words_list_test)-1 :
        trigramcentered = bigram + " " + Functions.is_number(lemmes_list_test[i+1])


    if "#end document" in lemme or "#begin document" in lemme:
        predictions_list.append(lemme)
        continue

    predictedWith = ""

    if trigramcentered in dictionary_trigramcentered_wordlemmelemme_word :
        predicted_word = dictionary_trigramcentered_wordlemmelemme_word[trigramcentered]
        trigramcenteredFound += 1
        predictedWith = "Trigram Centered"
    elif bigram in dictionary_bigram_wordlemme_word :
        predicted_word = dictionary_bigram_wordlemme_word[bigram]
        bigramFound += 1
        predictedWith = "Bigram"
    elif lemme in dictionary_lemme_word :
        predicted_word = dictionary_lemme_word[lemme]
        unigramFound += 1
        predictedWith = "Unigram"
    else:
        predicted_word = lemme
        monogramFound += 1
        predictedWith = "Lemme"

    previous_word = word
    previous_lemme = lemme
    previous_prediction = predicted_word
    predictions_list.append(predicted_word)

Log.debug(" ")

Log.debug("Trigram Centered found : "+str(trigramcenteredFound))
Log.debug("Bigram found : "+str(bigramFound))
Log.debug("Unigram found : "+str(unigramFound))
Log.debug("No combinaison found : "+str(monogramFound))
Log.debug(" ")

Functions.evaluate_predictions(words_list_test, predictions_list)

# Refining

if refine:

    Log.debug("Refining : ")

    for j in range(0,5):

        predictions_list = Functions.refine_predictions(lemmes_list_test, predictions_list, dictionary_trigramcentered_wordlemmeword_word)

        Functions.evaluate_predictions(words_list_test, predictions_list)

Log.debug("Done")



