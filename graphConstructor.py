"""
Name: João Pedro Simões Alegria
NMEC: 85048

Name: Filipe Neto Pires
NMEC: 85122

Auxiliary script used to construct graph to help in the data visualization.
Generates top 20 counting evolution for all three approaches and the probabilist approaches behavior.
"""

import sys
import csv
import math
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

    insource = args[0]
    if os.path.isdir(insource):
        ms = {}
        ds = {}
        for subfolder in os.listdir(insource):
            m, d = tuple(subfolder.split("_"))
            files = [insource+"/"+subfolder+"/" +
                     x for x in os.listdir(insource+"/"+subfolder)]
            file = open(files[0])
            csvfile = csv.reader(file)
            first = True
            cumSum = 0
            for line in csvfile:
                if first:
                    first = False
                    continue
                cumSum += float(line[3])
            ms[int(m)] = cumSum
            ds[int(d)] = cumSum

        ms = sorted(ms.items(), key=lambda tup: tup[0])
        ds = sorted(ds.items(), key=lambda tup: tup[0])
        print("ms", ms)
        print("ds", ds)
        plt.plot([x[0] for x in ms], [x[1] for x in ms], label="Columns")
        plt.legend(fontsize=35)
        plt.show()
        plt.plot([x[0] for x in ds], [x[1] for x in ds], label="Hashes")
        plt.legend(fontsize=35)
        plt.show()

    else:
        file = open(insource)
        csvfile = csv.reader(file)
        first = True
        terms = {}
        for line in csvfile:
            if first:
                first = False
                continue
            terms[line[0]] = [float(line[1]), float(line[2])]

        # compare top20 counts
        terms = sorted(
            terms.items(), key=lambda tup: tup[1][0], reverse=True)[:20]
        print(terms)
        label = [x[0] for x in terms]
        exact = [x[1][0] for x in terms]
        sketch = [x[1][1] for x in terms]

        index = np.arange(len(label))
        barwidth = 0.4
        plt.subplots()
        plt.bar(index, exact, barwidth, label="Exact")
        plt.bar(index+barwidth, sketch, barwidth, label="Sketch")
        plt.xticks(index+barwidth, label)
        plt.legend(fontsize=35)
        plt.tight_layout()
        plt.show()


if __name__ == "__main__":
    main(sys.argv[1:])
