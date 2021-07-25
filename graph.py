import numpy as np


def print_children(bios):
    for i in np.arange(len(bios)):
        print("'" + bios[i].name + "' children:")
        for j in np.arange(len(bios[i].children)):
            print(bios[j].name)
        print()

def add_children(bios,weights,n):
    for i in np.arange(len(bios)):
        for j in np.arange(len(bios)):
            if i != j:
                weight = 0
                for k in np.arange(len(bios[i].words)):
                    if bios[i].words[k] in bios[j].words:
                        weight += weights[bios[i].words[k]]
                if weight > n:
                    bios[i].appendchild(bios[j])
    return bios

def dfs(node,visited):
    visited.append(node)
    for i in node.children:
        if i not in visited:
            dfs(i,visited)
    return visited

def get_connected_comps(bios):
    ccomponents = []
    visited = []
    for i in np.arange(len(bios)):
        if bios[i] not in visited:
            comp = dfs(bios[i],[])
            visited += comp
            ccomponents.append(comp)
    return ccomponents

def print_comps(ccomponents,names):
    for i in np.arange(len(ccomponents)):
        print(names[i] + ":",end=" ")
        for j in np.arange(len(ccomponents[i])):
            print(ccomponents[i][j].name,end="")
            if j == len(ccomponents[i]) - 1:
                print()
            else:
                print(",",end=" ")
        print()

def determine_frequent_by_occurence(word,weight,mostfreq2,mostfreq2vals):
    if len(word) > 3:
        if weight > mostfreq2vals[1]:
            mostfreq2vals[1] = weight
            mostfreq2[1] = word
        if weight > mostfreq2vals[0]:
            tmp1 = mostfreq2vals[0]
            tmp2 = mostfreq2[0]
            mostfreq2vals[0] = weight
            mostfreq2[0] = word
            mostfreq2[1] = tmp2
            mostfreq2vals[1] = tmp1
    return mostfreq2,mostfreq2vals

def determine_frequent_by_log(word,weight,mostfreq2,mostfreq2vals):
    if len(word) > 3:
        if weight > mostfreq2vals[1]:
            mostfreq2vals[1] = weight
            mostfreq2[1] = word
        if weight > mostfreq2vals[0]:
            tmp1 = mostfreq2vals[0]
            tmp2 = mostfreq2[0]
            mostfreq2vals[0] = weight
            mostfreq2[0] = word
            mostfreq2[1] = tmp2
            mostfreq2vals[1] = tmp1
    return mostfreq2,mostfreq2vals

def get_name(comp,portertooriginal,weights):
    mostfreq2 = ["",""]
    mostfreq2vals = [0] * 2 # make sure initial vals will be smaller than any other word weight
    if len(comp) != 1: # not a singular node cluster
        alreadyseen = []
        for i in np.arange(len(comp)):
            for j in np.arange(len(comp[i].words)):
                if comp[i].words[j] not in alreadyseen:
                    jweight = 0
                    word = comp[i].words[j]
                    for k in np.arange(len(comp)):
                        if k != i:
                            jweight += comp[k].words.count(word)
                    alreadyseen.append(word)
                    mostfreq2,mostfreq2vals = determine_frequent_by_occurence(portertooriginal[word],jweight,mostfreq2,mostfreq2vals)
        return mostfreq2[0] + " " + mostfreq2[1]
    else: # for single node clusters you want as descriptive as possible, so you search for largest weight->least occuring bc you dont need to describe other nodes as well
        for i in np.arange(len(comp[0].words)):
            mostfreq2,mostfreq2vals = determine_frequent_by_log(portertooriginal[comp[0].words[i]],weights[comp[0].words[i]],mostfreq2,mostfreq2vals)
    return mostfreq2[0] + " " + mostfreq2[1]

def namecomps(ccomponents,portertooriginal,weights):
    names = [None] * len(ccomponents)
    for i in np.arange(len(ccomponents)):
        names[i] = get_name(ccomponents[i],portertooriginal,weights)
    return names

def graph(bios,weights,k,portertooriginal):
    bios = add_children(bios,weights,k)
    ccomponents = get_connected_comps(bios)
    names = namecomps(ccomponents,portertooriginal,weights)
    print_comps(ccomponents,names)