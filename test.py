from collections import defaultdict



import re
import nltk

import IntentDetector

'''''
word = 'requested amount  17000'
att='requested amount'
syn=''
msg='17000'
regularExp="(?i)"+att+"[ ]*[is|are|is with value|are with value]*[ ]*(?i)"+syn+"[ ]*(?i)"+msg
regexp = re.compile(regularExp)
if regexp.search(word):
  print ('matched')

test=defaultdict(dict)
test['request']['17000']='='
test['request']['12000']='>'
print(test['request'])

'''

DictPenalties={'CC':0.5, 'CD':1, 'DT':0, 'EX':1, 'FW':0, 'IN':0, 'JJ':0, 'JJR':0, 'JJS':0, 'LS':0, 'MD':2, 'NN':1, 'NNS':1,
               'NNP':1, 'NNPS':1, 'PDT':0, 'POS':0, 'PRP':2, 'PRP$':2, 'RB':0, 'RBR':0, 'RBS':0, 'RP':2, 'TO':1, 'UH':2,
               'VB':2, 'VBD':2, 'VBG':2, 'VBN':1, 'VBP':2, 'VBZ':2, 'WDT':0, 'WP':0, 'WP$':0, 'WRB':0}

def matchCountConditionContributionWithOrEqual(syn,num,msg):
    regularExp=syn+"[ ]*or equal[ ]*"+num+"[ ]*contribution|contributions[ |.|?]*"
    regexp = re.compile(regularExp)
    if regexp.search(msg):
        return 1
    return 0

def matchCountConditionContribution(syn,num,msg):
    regularExp=syn+"[ ]*"+num+"[ ]*contribution|contributions[ |?|.]*"
    regexp = re.compile(regularExp)
    if regexp.search(msg):
        return 1
    return 0


def matchOrderByContribution(syn,msg):
    if syn=='':
        return 0
    regularExp=syn+"[ ]*[ASC|DESC|asc|desc|ascending|descending]*[by|of|with|according to]*" \
                   "[the number of their|their|the number of|the number of actor's|the number of actor]*" \
                   "contribution|contributions[ |?|.]*"
    regexp = re.compile(regularExp)
    if regexp.search(msg):
        return 1
    return 0

def distPenalty(pos,index1,index2):
    i=index1
    dist=0
    while i<index2:
        penalty=DictPenalties[pos[i][1]]
        dist=dist+penalty
        i=i+1
    return dist



def wordsMinimumDistance(msg,w1,w2):
    if w1 in msg and w2 in msg:
        arrayofW1=msg.split(w1)
        arrayofW2=msg.split(w2)
        indexesofW1=[]
        indexesofW2=[]
        i=0
        lastindex = 0
        while i<len(arrayofW1):
            if i==0:
                indexesofW1.append(lastindex+len(arrayofW1[i].split()))
            else:
                indexesofW1.append(lastindex + len(w1.split(" ")) + len(arrayofW1[i].split()))
            lastindex = len(arrayofW1[i].split())
            i=i+1

        i = 0
        lastindex=0
        while i < len(arrayofW2):
            if i==0:
                indexesofW2.append(lastindex + len(arrayofW2[i].split()))
            else:
                indexesofW2.append(lastindex+len(w2.split(" "))+len(arrayofW2[i].split()))
            lastindex = len(arrayofW2[i].split())
            i = i + 1

        #part of speech tagging
        tokens = nltk.word_tokenize(msg)
        PoS= nltk.pos_tag(tokens)

        i = 0
        minDist=len(msg)-1
        while i<len(indexesofW1)-1:
            j=0
            while j<len(indexesofW2)-1:
                indexW1=indexesofW1[i]
                indexW2=indexesofW2[j]
                dist=0
                if indexW1<indexW2:
                    indexW1=indexW1+len(w1.split(" "))
                    dist=distPenalty(PoS,indexW1,indexW2)
                elif indexW2<indexW1:
                    indexW2=indexW2+len(w2.split(" "))
                    dist=distPenalty(PoS,indexW2,indexW1)
                else:
                    return -1
                if dist<minDist:
                    minDist=dist
                j=j+1
            i=i+1
        return minDist
    return -1

def wordsCloseness(msg,w1,w2,w3):
    if w1 in msg and w2 in msg and w3 in msg:
        distW1W2=wordsMinimumDistance(msg,w1,w2)
        distW1W3 = wordsMinimumDistance(msg, w1, w3)
        distW2W3 = wordsMinimumDistance(msg, w2, w3)
        print(w1+" "+w2+" "+str(distW1W2))
        print(w1 + " " + w3 + " " + str(distW1W3))
        print(w2 + " " + w3 + " " + str(distW2W3))
        if distW1W2==-1 or distW1W3==-1 or distW2W3==-1:
            return -1
        closeness=(distW1W2+distW1W3+distW2W3)/3
        return closeness

#print(matchCountConditionContribution('more than ',str(2),'more than 2 offers'))
print(wordsCloseness('which offer has offered amount and monthly cost less than 15000',
                           'less than','15000','offered amount'))




