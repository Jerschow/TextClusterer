# TextClusterer
A program that takes a file with short biographies of people and tries to cluster similar people together.
names of clusters were done as follows:
-if cluster had many nodes: find the 2 words with the most occurences in the cluster
-if cluster had 1 node: find the 2 words that appear the least in the entire input file using the weights dict

how to run:
python3 <kvalue> inputfilepath stopwords
kvalue is a required parameter that determines the minimum weight needed in order for 2 vertices (texts) to have an edge and stopwords is an optional parameter that ignores all words in the file stopwords.txt, that must be in the same directory as from where the command is run.
  
format of inputfile.txt:
title1
description1

title2
.
.
.

collaborators: I used Vivake Gupta's python porter stemming algorithm from: https://tartarus.org/martin/PorterStemmer/. porterstemmer.py is all his code and his code does not appear anywhere else in this repository.
