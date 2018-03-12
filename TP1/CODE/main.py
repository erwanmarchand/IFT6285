"""
    Docstring module
"""

from Log import *
import Log as Log_file
import gzip
import os

# pylint: disable=C0301

Log_file.DEBUG_ACTIVATED = True

# pylint: disable=C0103

Train_Path = "../DATAS/train"
Test_Path = "../DATAS/test"
Dev_Path = "../DATAS/dev"

# For final statistics

count_identical = 0
count_different = 0
percentage = 0

# Case to study

use_unigram = True
use_bigram = False
use_trigram = False 

# number of .gz file to consider for learning (out of 1500) (+1500 will act as 1500)
# the higher our n-gram is, the more RAM will be used, so number of learning files will have to be lower if we still want a fast computation

learning_files_to_consider = 1500

if learning_files_to_consider < 0 :
    learning_files_to_consider = 1
elif learning_files_to_consider > 1500 :
    learning_files_to_consider = 1500

# since we can't consider trigram withou considering bigram or bigram without unigram :

if use_trigram :
    use_bigram = True

if use_bigram :
    use_unigram = True

# Learning

dict_lemme_to_words = dict()

dict_bigram_wordlemme_to_words = dict()

dict_trigram_wordwordlemme_to_words = dict()

Log.debug("Learning")

tempBreak = 1

fileNumber = 0

for file in os.listdir(Train_Path):

    # if we don't use unigram, we are in the baseline case where we take lemme for our predicitons (just need to leave empty dictionnaries)
    if not use_unigram :
        break

    # break here if we learned with enough files
    if fileNumber == learning_files_to_consider:
        break

    if file.endswith(".gz"):
        fileNumber += 1
        Log.debug("Exploring File "+file+" "+str(fileNumber)+"/"+str(learning_files_to_consider),1)
        with gzip.open(Train_Path+"/"+file, 'rb') as f:
           file_content = f.read()

        file_content = str(file_content)
        file_lines = file_content.split("\\n")
        file_lines = file_lines[1:len(file_lines)-4]

        previousWord = "."
        previouspreviousWord = "."

        for line in file_lines :
            line_splited = line.split("\\t")
            word = line_splited[0].lower()
            lemme = line_splited[1].lower()

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

            if  ("." in previousWord or "," in previousWord or 
                "(" in previousWord or ")" in previousWord or 
                "{" in previousWord or "}" in previousWord or 
                "[" in previousWord or "]" in previousWord or 
                " " in previousWord or "!" in previousWord or 
                "?" in previousWord or ";" in previousWord ):
                previouspreviousWord = previousWord
                previousWord = word
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


            # TRIGRAM

            if not use_trigram:
                previousWord = word
                continue

            if  ("." in previouspreviousWord or "," in previouspreviousWord or
                "(" in previouspreviousWord or ")" in previouspreviousWord or
                "{" in previouspreviousWord or "}" in previouspreviousWord or
                "[" in previouspreviousWord or "]" in previouspreviousWord or
                " " in previouspreviousWord or "!" in previouspreviousWord or
                "?" in previouspreviousWord or ";" in previouspreviousWord ):
                previouspreviousWord = previousWord
                previousWord = word
                continue

            trigram_word_word_lemme = previouspreviousWord+" "+previousWord+" "+lemme

            if trigram_word_word_lemme in dict_trigram_wordwordlemme_to_words :
                dict_words_to_frequence = dict_trigram_wordwordlemme_to_words[trigram_word_word_lemme]
            else:
                dict_words_to_frequence = dict()
                dict_trigram_wordwordlemme_to_words[trigram_word_word_lemme] = dict_words_to_frequence

            if word in dict_words_to_frequence :
                dict_words_to_frequence[word] += 1
            else:
                dict_words_to_frequence[word] = 1

            previouspreviousWord = previousWord
            previousWord = word




Log.debug(" ")
Log.debug("Estimating most frequent words")

dictionary_lemme_word = dict()

for key1 in dict_lemme_to_words :
    dict_words_to_frequence = dict_lemme_to_words[key1]
    most_frequent_word = lemme
    frequence = 0
    for key, value in dict_words_to_frequence.items():
        if value > frequence :
            frequence = value
            most_frequent_word = key

    dictionary_lemme_word[key1] = most_frequent_word

dictionary_bigram_wordlemme_word = dict()

for key1 in dict_bigram_wordlemme_to_words :
    dict_words_to_frequence = dict_bigram_wordlemme_to_words[key1]
    most_frequent_word = lemme
    frequence = 0
    for key, value in dict_words_to_frequence.items():
        if value > frequence :
            frequence = value
            most_frequent_word = key

    dictionary_bigram_wordlemme_word[key1] = most_frequent_word

dictionary_tri_wordwordlemme_word = dict()

for key1 in dict_trigram_wordwordlemme_to_words :
    dict_words_to_frequence = dict_trigram_wordwordlemme_to_words[key1]
    most_frequent_word = lemme
    frequence = 0
    for key, value in dict_words_to_frequence.items():
        if value > frequence :
            frequence = value
            most_frequent_word = key

    dictionary_tri_wordwordlemme_word[key1] = most_frequent_word

# Testing

Log.debug(" ")
Log.debug("Testing")

fileNumber = 0

trigramFound = 0
bigramFound = 0
unigramFound = 0
monogramFound = 0

for file in os.listdir(Test_Path):

    if file.endswith(".gz"):
        fileNumber += 1
        Log.debug("Exploring File "+file+" "+str(fileNumber)+"/"+str(len(os.listdir(Test_Path))-1),1)
        with gzip.open(Test_Path+"/"+file, 'rb') as f:
           file_content = f.read()

        file_content = str(file_content)
        file_lines = file_content.split("\\n")
        file_lines = file_lines[1:len(file_lines)-4]

        previous_word = ""
        previous_lemme = ""
        previous_prediction = ""
        previous_previous_prediction = ""

        for line in file_lines :
            line_splited = line.split("\\t")
            word = line_splited[0].lower()
            lemme = line_splited[1].lower()

            bigram = previous_prediction+" "+lemme
            trigram = previous_previous_prediction+" "+previous_prediction+" "+lemme

            if "#end document" in word or "#begin document" in word:
                continue

            if trigram in dictionary_tri_wordwordlemme_word :
                predicted_word = dictionary_tri_wordwordlemme_word[trigram]
                trigramFound += 1
            elif bigram in dictionary_bigram_wordlemme_word :
                predicted_word = dictionary_bigram_wordlemme_word[bigram]
                bigramFound += 1
            elif lemme in dictionary_lemme_word :
                predicted_word = dictionary_lemme_word[lemme]
                unigramFound += 1
            else:
                predicted_word = lemme
                monogramFound += 1

            if predicted_word == word :
                count_identical += 1
            else :
                count_different += 1
                #Log.debug("Lemme : "+previous_lemme+" "+lemme + " --- Predicted word : "+previous_prediction+" "+predicted_word + " --- Actual word : "+previous_word+" "+word)

            previous_word = word
            previous_lemme = lemme
            previous_previous_prediction = previous_prediction
            previous_prediction = predicted_word


if (count_different*count_identical > 0):
    percentage = 100 * count_identical / (count_different+count_identical)

Log.debug(" ")

Log.debug("Trigram found : "+str(trigramFound))
Log.debug("Bigram found : "+str(bigramFound))
Log.debug("Unigram found : "+str(unigramFound))
Log.debug("No combinaison found : "+str(monogramFound))
Log.debug("Identical words : "+str(count_identical))
Log.debug("Different words : "+str(count_different))
Log.debug("Percentage : "+str(percentage))

Log.debug("Done")



