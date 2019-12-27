"""
Name: João Pedro Simões Alegria
NMEC: 85048

Auxiliary script used to construct graph to help in the data visualization.
Generates top 20 counting evolution for all three approaches and the probabilist approaches behavior.
"""

import sys
import csv
import getopt
import os
import matplotlib.pyplot as plt
import numpy as np


def main(argv):
    HELP = """
USAGE:
        python3 graphConstructor.py [-h] <inputFile>

ARGUMENTS:
    inputFile - result file used as source
"""

    try:
        opts, args = getopt.getopt(sys.argv[1:], "h")
    except getopt.GetoptError as err:
        print(HELP)
        sys.exit(2)

    if len(args) < 1:
        print(HELP)
        sys.exit(2)

    infile = args[0]

    file = open(infile)
    csvfile = csv.reader(file)
    first = True
    terms = {}
    counts = {}
    for line in csvfile:
        if first:
            first = False
            continue
        terms[line[0]] = [float(line[1]), float(line[5]), float(line[17])]
        counts[line[0]] = [float(line[1]), float(line[2]), float(line[14])]

    # compare top20 counts
    terms = sorted(terms.items(), key=lambda tup: tup[1][0], reverse=True)[:20]
    print(terms)
    label = [x[0] for x in terms]
    exact = [x[1][0] for x in terms]
    prob = [x[1][1] for x in terms]
    log = [x[1][2] for x in terms]

    index = np.arange(len(label))
    barwidth = 0.3
    plt.subplots()
    plt.bar(index, exact, barwidth, label="Exact")
    plt.bar(index+barwidth, prob, barwidth, label="Prob")
    plt.bar(index+2*barwidth, log, barwidth, label="Log")
    plt.xticks(index+barwidth, label)
    plt.legend(fontsize=35)
    plt.tight_layout()
    plt.show()

    # compare evolution graph
    counts = sorted(
        counts.items(), key=lambda tup: tup[1][0], reverse=True)
    label = [x[0] for x in counts]
    exact = [x[1][0] for x in counts]
    prob = [x[1][1] for x in counts]
    log = [x[1][2] for x in counts]

    plt.plot(exact, prob, label="Prob")
    plt.plot(exact, log, label="Log")
    plt.legend(fontsize=35)
    plt.show()


if __name__ == "__main__":
    main(sys.argv[1:])
