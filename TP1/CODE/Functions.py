from Log import *
import Log as Log_file
import os
import gzip

def is_number(s):
    try:
        float(s)
        return "a_number"
    except ValueError:
        return s
 

def extract_data_from_files(Path, learning_files_to_consider, splitDatas = False):

    Log.debug("Reading Files :")

    fileNumber = 0

    words_lemmes_list = []
    words_list = []
    lemmes_list = []

    for file in os.listdir(Path):

        # break here if we learned with enough files
        if fileNumber == learning_files_to_consider:
            break  

        if file.endswith(".gz"):
            fileNumber += 1
            Log.debug("Exploring File "+file+" "+str(fileNumber)+"/"+str(learning_files_to_consider),1)
            with gzip.open(Path+"/"+file, 'rb') as f:
                file_content = f.read()

            file_content = str(file_content)
            file_lines = file_content.split("\\n")
            file_lines = file_lines[1:len(file_lines)-4]


            for line in file_lines :
                line_splited = line.split("\\t")
                word = line_splited[0].lower()
                lemme = line_splited[1].lower()

                if not splitDatas :
                    words_lemmes_list.append([word,lemme])
                else :
                    words_list.append(word)
                    lemmes_list.append(lemme)

    if not splitDatas :
        return words_lemmes_list
    else :
        return words_list, lemmes_list

def generate_dictionary_from_frequences(dic_frequencies):

    dictionary = dict()

    for key1 in dic_frequencies :
        dict_words_to_frequence = dic_frequencies[key1]
        most_frequent_word = ""
        frequence = 0
        for key, value in dict_words_to_frequence.items():
            if value > frequence :
                frequence = value
                most_frequent_word = key

        dictionary[key1] = most_frequent_word
    
    return dictionary


def contain_stopword(word):
    return ("." in word or "," in word or
            "(" in word or ")" in word or
            "{" in word or "}" in word or
            "[" in word or "]" in word or
            " " in word or "!" in word or
            "?" in word or ";" in word)


def evaluate_predictions(word_list, prediciton_list):

    count_identical = 0
    count_different = 0
    percentage = 0

    for i in range(0, len(word_list)):

        if word_list[i] == prediciton_list[i] :
            count_identical += 1
        else :
            count_different += 1
            #Log.debug("Lemme : "+previous_lemme+" "+lemme + " --- Predicted word : "+previous_prediction+" "+predicted_word + " --- Actual word : "+previous_word+" "+word+ " --- Prediction Method : "+predictedWith)
            #Log.debug("Trigram Centered : "+trigramcentered+" --- Predicted word : "+predicted_word+ " --- Actual word : "+previous_word+" "+word+ " --- Prediction Method : "+predictedWith)


    if (count_different*count_identical > 0):
        percentage = 100 * count_identical / (count_different+count_identical)

    
    Log.debug("Evaluating Predictions :")
    Log.debug("Identical words : "+str(count_identical),1)
    Log.debug("Different words : "+str(count_different),1)
    Log.debug("Percentage : "+str(percentage),1)
    Log.debug(" ")


def refine_predictions(lemmes_list, prediciton_list, dictionary_wlw_to_w):

    for i in range(1, len(prediciton_list)-1):

        previous_word_predicted = prediciton_list[i-1]
        lemme = lemmes_list[i]
        next_word_predicted = prediciton_list[i+1]

        trigram = previous_word_predicted+" "+lemme+" "+next_word_predicted

        if trigram in dictionary_wlw_to_w :
            predicted_word = dictionary_wlw_to_w[trigram]
            prediciton_list[i] = predicted_word

    return prediciton_list