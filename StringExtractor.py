

class stringExtractor(object):
    def getName(s):
        node=""
        for letter in s:
            if(letter.isupper()):
                break
            node=node+letter
        return node
    def getRelationName(s):
        relation=""
        #eliminate relation word
        length=len(s)-7
        i=0
        while i<length-1:
            relation=relation+s[i]
            i=i+1
        return relation

    def getFirstAndLastChar(s):
        #return s[0].lower()+s[len(s)-1].lower()
        return s.lower()

    def getReturnedAttributeName(s):
        att=""
        #eliminate keyword word
        length=len(s)-6
        i=0
        while i<length-1:
            att=att+s[i]
            i=i+1
        return att

    def getAttributeName(s):
        att=''
        #eliminate Value word
        length=len(s)-4
        i=0
        while i<length-1:
            att=att+s[i]
            i=i+1
        return att

    def getNodeNameFromIntent(intent):
        nodeName=intent.split('_')[0]
        return nodeName





