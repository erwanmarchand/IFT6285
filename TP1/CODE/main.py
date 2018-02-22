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

count_identical = 0
count_different = 0
percentage = 0

Log.debug("Exploring Train files")

for file in os.listdir(Test_Path):
    if file.endswith(".gz"):
        with gzip.open(Test_Path+"/"+file, 'rb') as f:
           file_content = f.read()

        file_content = str(file_content)
        file_lines = file_content.split("\\n")
        file_lines = file_lines[1:len(file_lines)-4]



        for line in file_lines :
            line_splited = line.split("\\t")
            word = line_splited[0].lower()
            lemme = line_splited[1].lower()
            if word == lemme :
                count_identical += 1
            else :
                count_different += 1


if (count_different*count_identical > 0):
    percentage = 100 * count_identical / (count_different+count_identical)

Log.debug("Identical words : "+str(count_identical))
Log.debug("Different words : "+str(count_different))
Log.debug("Percentage : "+str(percentage))

Log.debug("Done")



