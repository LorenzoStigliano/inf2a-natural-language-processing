# File: statements.py
# Template file for Informatics 2A Assignment 2:
# 'A Natural Language Query System in Python/NLTK'

# John Longley, November 2012
# Revised November 2013 and November 2014 with help from Nikolay Bogoychev
# Revised November 2015 by Toms Bergmanis
# Revised October 2017 by Chunchuan Lyu


# PART A: Processing statements

def add(lst,item):
    if (item not in lst):
        lst.insert(len(lst),item)

class Lexicon:
    """stores known word stems of various part-of-speech categories"""
    def __init__ (self):
        self.listP = []
        self.listN = []
        self.listA = []
        self.listI = []
        self.listT = []
    
    def add(self,item,cat):
        
        if item==None :
            return
        elif cat == "P":
            add(self.listP,item)
        elif cat == "N":
            add(self.listN,item)
        elif cat == "A":
            add(self.listA,item) 
        elif cat == "I":
            add(self.listI,item)
        else:
            add(self.listT,item)

    def getAll(self,cat):
        if cat == "P":
            return self.listP
        elif cat == "N":
            return self.listN
        elif cat == "A":
            return self.listA 
        elif cat == "I":
            return self.listI
        else:
            return self.listT


class FactBase:
    """stores unary and binary relational facts"""
    def __init__ (self):
        self.Unary = []
        self.Binary = []

    def addUnary(self,pred,e1):
        add(self.Unary,(pred,e1))
    
    def addBinary(self,pred,e1,e2):
        add(self.Binary,(pred,e1,e2))
    
    def queryUnary(self,pred,e1):
        for i in self.Unary:
            if i == (pred,e1):
                return True
        return False

    def queryBinary(self,pred,e1,e2):
        for i in self.Binary:
            if i == (pred,e1,e2):
                return True
        return False

import re
from nltk.corpus import brown 
def verb_stem(s):
    """extracts the stem from the 3sg form of a verb, or returns empty string"""
    if re.match(".+([^sxyzaeiou]|[^cs][^hsxyzaeiou])s",s):
        ver = s[:-1]
    elif re.match(".+(a|e|i|o|u)ys",s):
        ver = s[:-1]
    elif re.match(".+[^aeiou]ies",s):
        ver = s[:-3]+"y"
    elif re.match("[^aeiou]ies",s):
        ver = s[:-1]
    elif re.match(".+(o|x|ch|sh|ss|zz)es",s):
        ver = s[:-2]
    elif re.match(".+([^s]s|[z^]z)es",s):
        ver = s[:-1]
    elif re.match("has",s):
        ver = "have"
    elif re.match(".+([^iosxz]|[^cs][^hiosxz])es",s):
        ver = s[:-1]
    else: return s
    
    for i in brown.tagged_words():
        if (ver, "VB") == i or (s, "VBZ") == i:
            return ver
    
    return ''
    

def add_proper_name (w,lx):
    """adds a name to a lexicon, checking if first letter is uppercase"""
    if ('A' <= w[0] and w[0] <= 'Z'):
        lx.add(w,'P')
        return ''
    else:
        return (w + " isn't a proper name")

def process_statement (lx,wlist,fb):
    """analyses a statement and updates lexicon and fact base accordingly;
       returns '' if successful, or error message if not."""
    # Grammar for the statement language is:
    #   S  -> P is AR Ns | P is A | P Is | P Ts P
    #   AR -> a | an
    # We parse this in an ad hoc way.
    msg = add_proper_name (wlist[0],lx)
    if (msg == ''):
        if (wlist[1] == 'is'):
            if (wlist[2] in ['a','an']):
                lx.add (wlist[3],'N')
                fb.addUnary ('N_'+wlist[3],wlist[0])
            else:
                lx.add (wlist[2],'A')
                fb.addUnary ('A_'+wlist[2],wlist[0])
        else:
            stem = verb_stem(wlist[1])
            if (len(wlist) == 2):
                lx.add (stem,'I')
                fb.addUnary ('I_'+stem,wlist[0])
            else:
                msg = add_proper_name (wlist[2],lx)
                if (msg == ''):
                    lx.add (stem,'T')
                    fb.addBinary ('T_'+stem,wlist[0],wlist[2])
    return msg
                        
# End of PART A.

