from parse import parse_and_check
from graph import graph


def start(fname,stopwords,k):
    print() # space below command line
    bios,weights,portertooriginal = parse_and_check(fname,stopwords)
    graph(bios,weights,k,portertooriginal)