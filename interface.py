import sys
from os import path
import main


fname = k = None
stopwords = []
for i in range(len(sys.argv)):
    try:
        tmp = int(sys.argv[i]) # test for error in casting. If error, then not specification for k
        if k != None:
            print("Error: Only 1 value for k allowed")
            exit(1)
        k = tmp
        continue
    except ValueError: # not specification for k
        pass
    if sys.argv[i] == "interface.py":
        continue
    elif sys.argv[i] == "stopwords":
        try:
            stopwords = open(sys.argv[i] + ".txt",'r').read().split(",")
        except FileNotFoundError:
            print("Error: No file in current directory called stopwords.txt")
            exit(1)
        for i in range(len(stopwords)):
            stopwords[i] = stopwords[i].strip().lower()
    else:
        if fname != None:
            print("Only 1 graph file allowed.")
            exit(1)
        if not path.isfile(sys.argv[i]):
            print("File does not exist: " + sys.argv[i])
            exit(1)
        fname = sys.argv[i]
if k == None:
    print("Error: need specification for k")
    exit(1)
if fname == None:
    print("Error: need input file")
    exit(1)
main.start(fname,stopwords,k)