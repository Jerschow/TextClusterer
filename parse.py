import numpy as np
from porterstemmer import PorterStemmer


class Node:
    def __init__(self,name,words,description):
        self.name = name.strip() # strip is to get rid of extraneous spaces on sides
        self.children = []
        self.description = description
        self.words = words

    def appendchild(self,child):
        self.children.append(child)

    def __str__(self):
        return self.name + "\n" + self.description


def remove_beginning_backslashes(rest):
    while rest != "" and rest[0] == "\n":
        rest = rest[1:]
    stop = False
    if rest == "":
        stop = True
    return rest,not stop

def return_false(rest):
    return rest,rest,rest,rest,False

def get_vars():
    name = description = ""
    s = [""]
    donewname = wasbackslash = False
    count = 0
    return name,description,s,donewname,count,wasbackslash

def addchar(char,donewname,name,s,description,count):
    if not donewname:
        name += char
    elif char.isalpha():
        s[-1] += char
    elif s[-1] != "": # make sure there are not 2 word breakers back to back, possibly generating an extraneous empty word
        s.append("")
    if donewname:
        description += char
    count += 1
    wasbackslash = False
    return name,s,description,count,wasbackslash

def readline(rest):
    rest,cont = remove_beginning_backslashes(rest)
    if not cont:
        return return_false(rest)
    name,description,s,donewname,count,wasbackslash = get_vars()
    for i in np.arange(len(rest)):
        char = rest[i]
        if wasbackslash and char == "\n":
            if description.strip() == "":
                print("Error: name of bio without description of bio")
                exit(1)
            return s,name,description,rest[count:],True
        if char == "\n":
            wasbackslash = donewname = True
            count += 1
            description += " "
            s.append("")
            continue
        name,s,description,count,wasbackslash = addchar(char,donewname,name,s,description,count)
    return s,name,description,rest[count:],True

def semantics(fname):
    bios = []
    f = open(fname,"r").read()
    words,name,description,f,cont = readline(f)
    return bios,f,words,name,description,f,cont

def parse(fname):
    bios,f,words,name,description,f,cont = semantics(fname)
    while cont:
        bios.append(Node(name,words,description))
        words,name,description,f,cont = readline(f)
    return bios

def print_bios(bios,weights):
    for i in range(len(bios)):
        print(bios[i].name)
        print(bios[i].words)
        print()
    keys = weights.keys()
    for i in keys:
        print("weight of word '" + i + "': " + str(weights[i]))
    print()

def check_remove(bios,i,j,word,stopwords):
    removed = False
    if word in stopwords or len(word) < 3:
        bios[i].words = bios[i].words[:j] + bios[i].words[j + 1:]
        removed = True
    return bios,removed

def porterstemming(bios,i,j,portertooriginal):
    word = bios[i].words[j].lower()
    pword = PorterStemmer().stem(word,0,len(word) - 1)
    portertooriginal[pword] = word
    bios[i].words[j] = pword
    return bios,pword,portertooriginal

def remove_or_modify(bios,i,j,stopwords,portertooriginal):
    bios,word,portertooriginal = porterstemming(bios,i,j,portertooriginal)
    bios,removed = check_remove(bios,i,j,portertooriginal[word],stopwords)
    return bios,word,removed,portertooriginal

def update_weights(word,thistext,weights):
    if word not in thistext:
        thistext.append(word)
        try:
            weights[word] += 1
        except KeyError:
            weights[word] = 1
    return weights,thistext

def prepare_occurences(bios,stopwords):
    weights = {}
    i = 0
    portertooriginal = {}
    while i < len(bios):
        thistext = []
        j = 0
        while j < len(bios[i].words):
            bios,word,removed,portertooriginal = remove_or_modify(bios,i,j,stopwords,portertooriginal)
            if removed:
                continue
            weights,thistext = update_weights(word,thistext,weights)
            j += 1
        i += 1
    return weights,bios,portertooriginal

def check(bios,i,j,weights,keys):
    word = bios[i].words[j]
    decrementj = False
    if weights[word] < 1: # in over half of bios
        bios[i].words = bios[i].words[:j] + bios[i].words[j + 1:]
        decrementj = True
        if word not in keys:
            keys.append(word)
    return keys,bios,decrementj

def prune_bios(bios,weights):
    i = 0
    keys = []
    while i < len(bios):
        j = 0
        while j < len(bios[i].words):
            keys,bios,cont = check(bios,i,j,weights,keys)
            if cont:
                continue
            j += 1
        i += 1
    return keys,bios

def prune_weights(weights,keys):
    for i in keys:
        del weights[i]
    return weights

def remove_words_over_half(bios,weights):
    keys,bios = prune_bios(bios,weights)
    weights = prune_weights(weights,keys)
    return bios,weights

def regularize_weights(weights,numbios):
    keys = weights.keys()
    for i in keys:
        weights[i] = - np.log2(weights[i] / numbios)
    return weights

def log_weights(bios,weights):
    weights = regularize_weights(weights,len(bios))
    bios,weights = remove_words_over_half(bios,weights) # removes words present in over half of bios
    return weights,bios

def regularize(bios,stopwords):
    weights,bios,portertooriginal = prepare_occurences(bios,stopwords)
    weights,bios = log_weights(bios,weights)
    return bios,weights,portertooriginal

def parse_and_check(fname,stopwords):
    bios = []
    try:
        bios = parse(fname)
    except:
        print("\nError: graph file not a txt file or a different error, listed above, occurred\n")
        exit(1)
    bios,weights,portertooriginal = regularize(bios,stopwords)
    return bios,weights,portertooriginal