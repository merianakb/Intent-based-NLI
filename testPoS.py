import nltk
#nltk.download('punkt')
#nltk.download('averaged_perceptron_tagger')

DictPenalties={'CC':0.5, 'CD':1, 'DT':0, 'EX':1, 'FW':0, 'IN':0, 'JJ':0, 'JJR':0, 'JJS':0, 'LS':0, 'MD':2, 'NN':1, 'NNS':1,
               'NNP':1, 'NNPS':1, 'PDT':0, 'POS':0, 'PRP':2, 'PRP$':2, 'RB':0, 'RBR':0, 'RBS':0, 'RP':2, 'TO':1, 'UH':2,
               'VB':2, 'VBD':2, 'VBG':2, 'VBN':1, 'VBP':2, 'VBZ':2, 'WDT':0, 'WP':0, 'WP$':0, 'WRB':0}

def distPenalty(pos,index1,index2):
    i=index1
    dist=0
    while i<index2:
        penalty=DictPenalties[pos[i][1]]
        dist=dist+penalty
        i=i+1
    return dist

msg='which applications have at least 2 offers'
msg1='which applications have requested amount greater than 15000'
msg2='which application have 2 canceled offers'
msg3='which offer has offered amount and monthly cost less than 15000'
msg4='which offer has offered amount and first withdrawal amount 15000 minimum'
msg5='Which actors are involved in each application having 2 offers minimum and an amount exceeding 15000.'
msg6='which applications have requested amount 15000 and at least 2 canceled offers'
msg7='which applications have 2 canceled offers and amount higher than 15000'

tokens=nltk.word_tokenize (msg3)

print("Part of Specch: ", nltk.pos_tag(tokens))
print(distPenalty(nltk.pos_tag(tokens),9,10))

