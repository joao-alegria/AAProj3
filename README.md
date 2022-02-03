# Frequent Items Counting
A Study on Memory-Efficient Algorithms

![](https://img.shields.io/badge/Academical%20Project-Yes-success)
![](https://img.shields.io/badge/Made%20With-Python-blue)
[![](https://img.shields.io/badge/Dataset-Project%20Gutenberg-lightgrey.svg?style=flat)](https://www.gutenberg.org/)
![](https://img.shields.io/badge/License-Free%20To%20Use-green)
![](https://img.shields.io/badge/Maintained-No-red)

## Description

Determining the most frequent items on a data stream has many applications and is a hot topic on the research community of the field.
The challenges inherent of data stream processing in a memory efficient way are very much worth exploring and some of the existing solutions already provide with great optimization strategies.

In this project, we focus on one of the most famous approximate counters to determine an estimation of the most frequent words of literary works from several authors in several languages and compare it to an exact counter. We also present a few conclusions drawn from the study applied to the dataset.

## Repository Structure

/dataset - literary works taken from [Project Gutenberg](https://www.gutenberg.org/) used as input data

/out - contains the programs' output

/report - the written report on the study conducted is made available here

/src - contains the source code, written in Python

## Instructions to Run 

First install all required packages:

```
$ pip3 install -r requirements
```

To run the word counting program, execute the following command:

```
$ python frequentWordFinder.py -d 1 -m 100 aliceInput/

```

## Authors

The authors of this repository are Filipe Pires and João Alegria, and the project was developed for the Advanced Algorithms Course of the Master's degree in Informatics Engineering of the University of Aveiro.

For further information, please read our [report](https://github.com/FilipePires98/FastCount/blob/master/report/report.pdf) or contact us at filipesnetopires@ua.pt or joao.p@ua.pt.
