Before running any program please install the necessary dependencies by running:
```
$ pip3 install -r requirements
```

To run the word counting program do:

```
$ python3 bookWordCounter.py -o myOut -r 100 aliceInput/
```

or 

```
$ python3 bookWordCounter.py -o myOut -p 0.5 -b 10 -r 100 aliceInput/
```


To analyze the top 20 most frequent words across all translations do:
```
$ python3 langAnalyzer.py aliceInput/
```