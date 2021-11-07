# File: pos_tagging.py
# Template file for Informatics 2A Assignment 2:
# 'A Natural Language Query System in Python/NLTK'

# John Longley, November 2012
# Revised November 2013 and November 2014 with help from Nikolay Bogoychev
# Revised November 2015 by Toms Bergmanis


# PART B: POS tagging

from statements import *

# The tagset we shall use is:
# P  A  Ns  Np  Is  Ip  Ts  Tp  BEs  BEp  DOs  DOp  AR  AND  WHO  WHICH  ?

# Tags for words playing a special role in the grammar:

function_words_tags = [('a','AR'), ('an','AR'), ('and','AND'),
     ('is','BEs'), ('are','BEp'), ('does','DOs'), ('do','DOp'), 
     ('who','WHO'), ('which','WHICH'), ('Who','WHO'), ('Which','WHICH'), ('?','?')]
     # upper or lowercase tolerated at start of question.

function_words = [p[0] for p in function_words_tags]


def unchanging_plurals():

    nnlist = []
    nnslist = []
    uplist=[]

    with open("sentences.txt", "r") as f:
        for line in f:
            linesplit = line.split()
            for i in linesplit:
                if re.match(r".*\|NN$",i):
                    add(nnlist,(i[:-3]))
                elif re.match(r".*\|NNS$",i):
                    add(nnslist,i[:-4])
    
    for i in nnlist:
        if i in nnslist:
            add(uplist,i)
    
    return uplist

unchanging_plurals_list = unchanging_plurals()

def noun_stem (s):
    """extracts the stem from a plural noun, or returns empty string"""
    if s in  unchanging_plurals_list:
        return s
    elif re.match(".*men",s):
        return s[:-3]+"man"    
    elif re.match(".*([^sxyzaeiou]|[^cs][^hsxyzaeiou])s",s):
        return s[:-1]
    elif re.match(".(ay|ey|iy|oy|uy)s",s):
        return s[:-1]
    elif re.match("..*[^aeiou]ies",s):
        return s[:-3]+"y"
    elif re.match("[^aeiou]ies",s):
        return s[:-1]
    elif re.match(".*(o|x|ch|sh|ss|zz)es",s):
        return s[:-2]
    elif re.match(".*([^s]s|[z^]z)es",s):
        return s[:-1]
    elif re.match("has",s):
        return "have"
    elif re.match(".*([^iosxz]|[^cs][^hiosxz])es",s):
        return s[:-1]
    else: return s

def tag_word (lx,wd):
    """returns a list of all possible tags for wd relative to lx"""
    listoftags=[]

    for i in function_words_tags :
        if wd == i[0]:
            add(listoftags, i[1])

    if wd in lx.getAll("P"):
        add(listoftags,"P")

    if wd in lx.getAll("A"):
        add(listoftags,"A")
    
    if wd in lx.getAll("I"):
        add(listoftags,"Ip")
    
    if verb_stem(wd) in lx.getAll("I"):
        add(listoftags,"Is")
    
    if wd in lx.getAll("T"):
        add(listoftags,"Tp")
    
    if verb_stem(wd) in lx.getAll("T"):
        add(listoftags,"Ts")
    
    if wd in lx.getAll("N"):
        add(listoftags,"Np")
    
    if noun_stem(wd) in lx.getAll("N"):
        add(listoftags,"Ns")
    
    return listoftags

def tag_words (lx, wds):
    """returns a list of all possible taggings for a list of words"""
    if (wds == []):
        return [[]]
    else:
        tag_first = tag_word (lx, wds[0])
        tag_rest = tag_words (lx, wds[1:])
        return [[fst] + rst for fst in tag_first for rst in tag_rest]

# End of PART B.