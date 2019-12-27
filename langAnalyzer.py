"""
Name: João Pedro Simões Alegria
NMEC: 85048

Auxiliary script that evaluates the top 20 most frequent word in the translations of a book and translates them to english.
"""

from translate import Translator
import csv
import sys
import getopt
import os

translator = Translator(provider="mymemory",
                        from_lang="autodetect", to_lang="en")


def main(argv):
    HELP = """
USAGE:
        python3 langAnalyzer.py [-h] <inputFolder>

ARGUMENTS:
    inputFolder - folder where the books to be processed should be present
"""

    try:
        opts, args = getopt.getopt(sys.argv[1:], "h")
    except getopt.GetoptError as err:
        print(HELP)
        sys.exit(2)

    if len(args) < 1:
        print(HELP)
        sys.exit(2)

    infolder = args[0]
    files = [infolder + x for x in os.listdir(infolder)]

    for f in files:
        file = open(f)
        csvfile = csv.reader(file)
        first = True
        terms = {}
        for line in csvfile:
            if first:
                first = False
                continue
            terms[line[0]] = float(line[1])

        terms = sorted(terms.items(), key=lambda tup: tup[1], reverse=True)
        terms = [x[0] for x in terms[:20]]

        print(f, end=":")
        for t in terms:
            trans = translator.translate(t)
            if trans == "PLEASE SELECT TWO DISTINCT LANGUAGES":
                print((t, t), end=";")
                continue
            print((trans.lower(), t), end=";")
        print()


if __name__ == "__main__":
    main(sys.argv[1:])
