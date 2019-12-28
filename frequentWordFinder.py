"""
Name: João Pedro Simões Alegria
NMEC: 85048

Name: Filipe Neto Pires
NMEC: 85122

Main Script that counts the words of a given book
Uses exact counting, fixed probability counting and decreasing logarithmic probability counting.
"""

import random
import math
import os
import sys
import re
import string
import getopt
from stop_words import get_stop_words
from langdetect import detect
from count_min_sketch import CountMinSketch


def countAll(wordCount, word):
    if word not in wordCount:
        wordCount[word] = 1
    else:
        wordCount[word] += 1


def detectLang(filename):
    maxTries = 10
    file = open(filename)
    tmpDecision = []
    for line in file:
        if line == "" or line == "\n":
            continue
        line = re.sub(r'\_', " ", re.sub(
            r"[^\w\s]", " ", line.strip().lower()))
        lang = detect(line)
        if len(tmpDecision) < maxTries:
            tmpDecision.append(lang)
        else:
            break
    lang = ""
    countLang = 0
    for l in set(tmpDecision):
        if tmpDecision.count(l) > countLang:
            countLang = tmpDecision.count(l)
            lang = l
    return lang


def findFrequentWords(filename, outputfile, numHash, numColumns):
    ALLCOUNT = {}
    MINSKETCHCOUNT = {}
    lang = detectLang(filename)
    stopWords = get_stop_words(lang)
    f = open(filename)
    allCount = {}
    minSketchCount = {}
    countMinSketch = CountMinSketch(numColumns, numHash)
    for line in f:
        if line == "" or line == "\n":
            continue
        line = re.sub(r'\_', " ", re.sub(
            r"[^\w\s]", " ", line.strip().lower()))
        line = re.split(r" +", line)
        for word in line:
            if len(word) > 1 and word not in stopWords:
                countAll(allCount, word)
                countMinSketch.update(word)
    for k in allCount:
        ALLCOUNT[k] = [allCount[k]]
        MINSKETCHCOUNT[k] = [countMinSketch.query(k)]
    f.close()

    out = open(outputfile, "w")
    out.write(
        "Key,All,Sketch,SketchMeanAbsEr,SketchMeanRelEr\n")
    for key in ALLCOUNT:
        avgAll = round(sum(ALLCOUNT[key])/len(ALLCOUNT[key]), 2)
        avgSketch = round(sum(MINSKETCHCOUNT[key])/len(MINSKETCHCOUNT[key]), 2)

        sketchError = [MINSKETCHCOUNT[key][i]-ALLCOUNT[key][i]
                       for i in range(len(ALLCOUNT[key]))]

        sketchMeanAbsEr = sum(sketchError)/len(sketchError)

        sketchMeanRelEr = (sketchMeanAbsEr/avgAll)*100

        out.write("{},{},{},{},{}\n".format(key, round(avgAll), round(
            avgSketch, 2), round(sketchMeanAbsEr, 2), round(sketchMeanRelEr, 2)))
    out.close()


def main(argv):
    HELP = """
USAGE:
        python3 frequentWordFinder.py [-h] [-o outputFolder] [-d numHash] [-m numColumns] <inputFolder>

ARGUMENTS:
    inputFolder - folder where the books to be processed should be present
OPTIONS:
    outputFolder -  defines the folder where the resulting files should be stores(default -> out)
    numHash -  number of hash functions used in the count-min sketch strategy
    numColumns -  number of columns used in the count-min sketch strategy
"""

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hd:m:o:")
    except getopt.GetoptError as err:
        print(HELP)
        sys.exit(2)

    outfolder = "out/"
    numHash = 5
    numColumns = 1000
    for o, a in opts:
        if o == "-o":
            outfolder = a
        elif o == "-d":
            numHash = int(a)
        elif o == "-m":
            numColumns = int(a)
        elif o == "-h":
            print(HELP)
            sys.exit(3)
    if len(args) < 1:
        print(HELP)
        sys.exit(1)

    if not os.path.exists(outfolder):
        os.makedirs(outfolder)
    infolder = args[0]

    files = [infolder + x for x in os.listdir(infolder)]
    outfiles = [outfolder + "/" + x+"Out.csv" for x in os.listdir(infolder)]

    if not os.path.exists(outfolder):
        os.makedirs(outfolder)

    for idx, filename in enumerate(files):
        findFrequentWords(
            filename, outfiles[idx], numHash, numColumns)


if __name__ == "__main__":
    main(sys.argv[1:])
