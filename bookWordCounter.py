"""
Name: João Pedro Simões Alegria
NMEC: 85048

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


def countAll(wordCount, word):
    if word not in wordCount:
        wordCount[word] = 1
    else:
        wordCount[word] += 1


def countProb(wordCount, word, prob):
    if random.random() <= prob:
        if word not in wordCount:
            wordCount[word] = 1
        else:
            wordCount[word] += 1


def countLog(wordCount, word, base):
    if word not in wordCount:
        wordCount[word] = 1
    else:
        count = wordCount[word]
        if random.random() <= 1/(base**count):
            wordCount[word] += 1


def detectLang(filename):
    maxTries = 10
    file = open(filename)
    tmpDecision = []
    for line in file:
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


def countBookWords(filename, outputfile, numRuns, probability, base):
    ALLCOUNT = {}
    PROBCOUNT = {}
    LOGCOUNT = {}
    lang = detectLang(filename)
    stopWords = get_stop_words(lang)
    for _ in range(numRuns):
        f = open(filename)
        allCount = {}
        probCount = {}
        logCount = {}
        for line in f:
            line = re.sub(r'\_', " ", re.sub(
                r"[^\w\s]", " ", line.strip().lower()))
            line = re.split(r" +", line)
            for word in line:
                if len(word) > 1 and word not in stopWords:
                    countAll(allCount, word)
                    countProb(probCount, word, probability)
                    countLog(logCount, word, base)

        for k in allCount:
            if k in ALLCOUNT:
                ALLCOUNT[k].append(allCount[k])
            else:
                ALLCOUNT[k] = [allCount[k]]

        for k in allCount:
            if k in PROBCOUNT:
                PROBCOUNT[k].append(probCount.get(k, 0))
            else:
                PROBCOUNT[k] = [probCount.get(k, 0)]

        for k in allCount:
            if k in LOGCOUNT:
                LOGCOUNT[k].append(logCount.get(k, 0))
            else:
                LOGCOUNT[k] = [logCount.get(k, 0)]
        f.close()

    out = open(outputfile, "w")
    out.write(
        "Key,All,ProbMean,ProbMin,ProbMax,ProbEst,ProbEstMin,ProbEstMax,ProbMeanAbsDev,ProbStdDev,ProbMaxDev,ProbVar,ProbMeanAbsEr,ProbMeanRelEr,LogMean,LogMin,LogMax,LogEst,LogEstMin,LogEstMax,LogMaxAbsDev,LogStdDev,LogMaxDev,LogVar,LogMeanAbsEr,LogMeanRelEr\n")
    for key in ALLCOUNT:
        avgAll = round(sum(ALLCOUNT[key])/len(ALLCOUNT[key]), 2)
        avgProb = round(sum(PROBCOUNT[key])/len(PROBCOUNT[key]), 2)
        avgLog = round(sum(LOGCOUNT[key])/len(LOGCOUNT[key]), 2)

        probEst = [x/probability for x in PROBCOUNT[key]]
        logEst = [(base**x)-1 for x in LOGCOUNT[key]]

        avgProbEst = sum(probEst)/len(probEst)
        avgLogEst = sum(logEst)/len(logEst)

        probDev = [abs(x-avgProbEst) for x in probEst]
        logDev = [abs(x-avgLogEst) for x in logEst]
        probMAD = sum(probDev)/len(probDev)
        logMAD = sum(logDev)/len(logDev)
        probStdDev = math.sqrt(sum(x**2 for x in probDev)/len(probDev))
        logStdDev = math.sqrt(sum(x**2 for x in logDev)/len(logDev))

        probError = [ALLCOUNT[key][i]-probEst[i]
                     for i in range(len(ALLCOUNT[key]))]
        logError = [ALLCOUNT[key][i]-logEst[i]
                    for i in range(len(LOGCOUNT[key]))]

        probMeanAbsEr = sum(probError)/len(probError)
        logMeanAbsEr = sum(logError)/len(logError)

        probMeanRelEr = probMeanAbsEr/avgAll
        logMeanRelEr = logMeanAbsEr/avgAll

        out.write("{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}\n".format(key, round(avgAll), round(avgProb, 3), round(min(PROBCOUNT[key])), round(max(PROBCOUNT[key])), round(avgProbEst, 3), round(min(probEst), 3), round(max(probEst), 3), round(probMAD, 3), round(probStdDev, 3), round(max(probDev), 2), round(
            probStdDev**2, 3), round(probMeanAbsEr, 3), round(probMeanRelEr, 3), round(avgLog, 3), round(min(LOGCOUNT[key]), 3), round(max(LOGCOUNT[key]), 3), round(avgLogEst, 3), round(min(logEst), 3), round(max(logEst), 3), round(logMAD, 3), round(logStdDev, 3), round(max(logDev), 3), round(logStdDev**2, 3), round(logMeanAbsEr, 3), round(logMeanRelEr, 3)))
    out.close()


def main(argv):
    HELP = """
USAGE:
        python3 bookWordCounter.py [-h] [-o outputFolder] [-p fixedProbability] [-b decreasingProbabilityBase] [-r numRuns] <inputFolder>

ARGUMENTS:
    inputFolder - folder where the books to be processed should be present
OPTIONS:
    outputFolder -  defines the folder where the resulting files should be stores(default -> out)
    numRuns -  number of runs the counting process should be executed
    fixedProbability -  probability used in the fixed probability approach
    decreasingProbabilityBase -  base used when calculating in the decreasing probability approach
"""

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hr:p:b:o:")
    except getopt.GetoptError as err:
        print(HELP)
        sys.exit(2)

    numRuns = 1000
    probability = 1/32
    base = 2
    outfolder = "out/"
    for o, a in opts:
        if o == "-r":
            numRuns = int(a)
        elif o == "-o":
            outfolder = a
        elif o == "-b":
            base = float(a)
        elif o == "-p":
            probability = float(a)
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
        countBookWords(filename, outfiles[idx], numRuns, probability, base)


if __name__ == "__main__":
    main(sys.argv[1:])
