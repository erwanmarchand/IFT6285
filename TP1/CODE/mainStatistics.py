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

count_identical = 0
count_different = 0
percentage = 0

# Learning

dict_lemme_to_words = dict()

Log.debug("Learning")

tempBreak = 1

fileNumber = 0

for file in os.listdir(Train_Path):

    #if fileNumber == 10:
    #    break

    if file.endswith(".gz"):
        fileNumber += 1
        Log.debug("Exploring File "+file+" "+str(fileNumber)+"/"+str(len(os.listdir(Train_Path))-1),1)
        with gzip.open(Train_Path+"/"+file, 'rb') as f:
           file_content = f.read()

        file_content = str(file_content)
        file_lines = file_content.split("\\n")
        file_lines = file_lines[1:len(file_lines)-4]

        for line in file_lines :
            line_splited = line.split("\\t")
            word = line_splited[0].lower()
            lemme = line_splited[1].lower()

            if "#end document" in word or "#begin document" in word:
                continue

            if lemme in dict_lemme_to_words :
                dict_words_to_frequence = dict_lemme_to_words[lemme]
            else:
                dict_words_to_frequence = dict()
                dict_lemme_to_words[lemme] = dict_words_to_frequence

            if word in dict_words_to_frequence :
                dict_words_to_frequence[word] += 1
            else:
                dict_words_to_frequence[word] = 1

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

# Testing

Log.debug(" ")
Log.debug("Testing")

fileNumber = 0

for file in os.listdir(Test_Path):

    if file.endswith(".gz"):
        fileNumber += 1
        Log.debug("Exploring File "+file+" "+str(fileNumber)+"/"+str(len(os.listdir(Test_Path))-1),1)
        with gzip.open(Test_Path+"/"+file, 'rb') as f:
           file_content = f.read()

        file_content = str(file_content)
        file_lines = file_content.split("\\n")
        file_lines = file_lines[1:len(file_lines)-4]

        for line in file_lines :
            line_splited = line.split("\\t")
            word = line_splited[0].lower()
            lemme = line_splited[1].lower()

            if "#end document" in word or "#begin document" in word:
                continue

            if lemme in dictionary_lemme_word :
                predicted_word = dictionary_lemme_word[lemme]
            else:
                predicted_word = lemme

            if predicted_word == word :
                count_identical += 1
            else :
                count_different += 1
                #Log.debug(lemme + " --- "+predicted_word + " --- "+word)


if (count_different*count_identical > 0):
    percentage = 100 * count_identical / (count_different+count_identical)

Log.debug(" ")

Log.debug("Identical words : "+str(count_identical))
Log.debug("Different words : "+str(count_different))
Log.debug("Percentage : "+str(percentage))

Log.debug("Done")



