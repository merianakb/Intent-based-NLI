import time
from collections import defaultdict


import Dictionary
import IntentEntitiesInfos

from E0_Category import  e0Category
from E1_Category import e1Category
from StringExtractor import stringExtractor


import re
import nltk


threshold=0.34
DictPenalties={'CC':0.5, 'CD':1, 'DT':0, 'EX':1, 'FW':0, 'IN':0, 'JJ':0, 'JJR':0, 'JJS':0, 'LS':0, 'MD':2, 'NN':1, 'NNS':1,
               'NNP':1, 'NNPS':1, 'PDT':0, 'POS':0, 'PRP':2, 'PRP$':2, 'RB':0, 'RBR':0, 'RBS':0, 'RP':2, 'TO':1, 'UH':2,
               'VB':2, 'VBD':2, 'VBG':2, 'VBN':1, 'VBP':2, 'VBZ':2, 'WDT':1, 'WP':1, 'WP$':1, 'WRB':1, '.':2, ',':2}

DictPenalties2={'CC':0.5, 'CD':1, 'DT':1, 'EX':1, 'FW':0, 'IN':1, 'JJ':1, 'JJR':1, 'JJS':1, 'LS':0, 'MD':2, 'NN':1, 'NNS':1,
               'NNP':1, 'NNPS':1, 'PDT':0, 'POS':0, 'PRP':2, 'PRP$':2, 'RB':1, 'RBR':1, 'RBS':1, 'RP':2, 'TO':1, 'UH':2,
               'VB':2, 'VBD':2, 'VBG':2, 'VBN':1, 'VBP':2, 'VBZ':2, 'WDT':1, 'WP':1, 'WP$':1, 'WRB':1, '.':2, ',':2}

def get_maxConfidence_entities(response,entity):
        max_confidence=0
        index_entity=0
        i=0
        for ent in response['entities'][entity]:
            if(ent['confidence']>max_confidence):
                max_confidence=ent['confidence']
                index_entity=i
            i=i+1
        return index_entity

def get_returned_attributes(response,node,entityAttributes,numericalValueOperator):
    for item in response['entities']:
        str_item=str(item) #positionType:positionType
        str_item=str_item.split(':')[0]
        if(str_item.endswith("KeyWord") and str_item.startswith(node)):
            att=stringExtractor.getReturnedAttributeName(str_item)
            if att not in entityAttributes and att not in numericalValueOperator:
                returned_attributes.append(att)
    return returned_attributes

def aggregationSyn(msg):
    synonymes=['for each','per','by each','in each','of each','in processing each']
    for item in synonymes:
        if item in msg:
            return item
    return ''

def lessThanSyn(msg):
    synonymes=['less than or equal','lesser or equal','lesser than or equal','lower or equal','lower than or equal',
                'less than','lesser','lesser than','lower','lower than','maximum',' max ','below','under','at most']
    detectedSynon=[]
    for item in synonymes:
        if item in msg:
            detectedSynon.insert(0,item)
    return detectedSynon

def greaterThanSyn(msg):
    synonymes=['greater than or equal','greater or equal','more than or equal',
                'greater than','greater','exceeding','excess','above','minimum',' min ','more than','at least']
    detectedSynon=[]
    for item in synonymes:
        if item in msg:
            detectedSynon.insert(0,item)
    return detectedSynon

def equalSyn(msg):
    synonymes=['equal to','equal']
    detectedSynon=[]
    for item in synonymes:
        if item in msg:
            detectedSynon.insert(0,item)
    return detectedSynon

def orderBySyn(msg):
    synonymes=['ordered','order','sorted','sort','ascending order','descending order','ASC','DESC','asc','desc','ascending','descending']
    for item in synonymes:
        if item in msg:
            return item
    return ''

def DESCSymbSyn(msg):
    synonymes=['DESC','desc','descending']
    for item in synonymes:
        if item in msg:
            return item
    return ''


def matchAttEqValue(attribute,value,msg):
    attribute=attribute.lower()
    msg=msg.lower()
    regularExp = attribute +"[ ]*" + value + "[?]*"
    regexp = re.compile(regularExp)
    if regexp.search(msg):
        return 1
    return 0

def matchCountCondition(node,num,relationDetected,msg):
    node=node.lower()
    msg=msg.lower()
    regularExp=num+"[ ]*[A-Za-z]*[ ]*"+node
    regexp = re.compile(regularExp)
    if regexp.search(msg):
        return 1
    '''''
    for rel in relationDetected:
        regularExp=num+"[ ]*"+rel+"[ ]*"+node
        regexp = re.compile(regularExp)
        if regexp.search(msg):
            return 1
        '''
    return 0


def matchOrderBy(syn,entity,msg):
    if syn=='':
        return 0
    #regularExp=syn+"[ ]*[ASC|DESC|asc|desc|ascending|descending]*[by|of|with|according to]*" \
                  # "[the|their|the values of|the value of|values of|value of]*[ ]*"+attribute+"[ |?|.]*"
    regularExp=syn+".*"+entity+".*"
    regexp = re.compile(regularExp)
    if regexp.search(msg):
        return 1
    return 0


def getOrderByAttributeOrNode(orderBySyn,nodeAndAttributeDetected,AttributeNum,nodeDetected,msg):
    for entity in nodeAndAttributeDetected:
        if matchOrderBy(orderBySyn,entity,msg):
            if entity in AttributeNum.keys():
                return AttributeNum[entity],''
            elif entity in nodeDetected.keys():
                return '',nodeDetected[entity]
    return '',''

def distPenalty(pos,index1,index2, dictPenalties):
    i=index1
    dist=0
    while i<index2:
        penalty=dictPenalties[pos[i][1]]
        dist=dist+penalty
        i=i+1
    return dist

def wordsMinimumDistance(msg,w1,w2, dicPenalties):
    if w1 in msg and w2 in msg:
        if w1=='' or w2 =='':
            return 0
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

        if (w1 == 'application' and w2 == 'maximum'):
            print(PoS)

        i = 0
        minDist=len(msg)-1
        while i<len(indexesofW1)-1:
            j=0
            while j<len(indexesofW2)-1:
                indexW1=indexesofW1[i]
                indexW2=indexesofW2[j]
                if indexW1<indexW2:
                    indexW1=indexW1+len(w1.split(" "))
                    dist=distPenalty(PoS,indexW1,indexW2,dicPenalties)
                elif indexW2<indexW1:
                    indexW2=indexW2+len(w2.split(" "))
                    dist=distPenalty(PoS,indexW2,indexW1,dicPenalties)
                else:
                    return -1
                if dist<minDist:
                    minDist=dist
                j=j+1
            i=i+1
        return minDist
    return -1

def wordsCloseness(msg,w1,w2,w3,dicPenalties):
    msg=msg.lower()
    w1=w1.lower()
    w2=w2.lower()
    w3=w3.lower()
    print(w1+" "+w2+" "+w3)
    if w1 in msg and w2 in msg and w3 in msg:

        distW1W2=wordsMinimumDistance(msg,w1,w2,dicPenalties)
        distW1W3 = wordsMinimumDistance(msg, w1, w3,dicPenalties)
        distW2W3 = wordsMinimumDistance(msg, w2, w3,dicPenalties)
        if distW1W2==-1 or distW1W3==-1 or distW2W3==-1:
            return -1
        closeness=(distW1W2+distW1W3+distW2W3)/3
        return closeness
    return -1

def getAttributeValueOperator(activityTimeCondition,AttributeNum,numValues,greaterThanSyn,lessThanSyn,equalSyn,msg):
    print()
    print(AttributeNum)
    print(numValues)
    print()
    attValueOperator=activityTimeCondition
    for att in AttributeNum:
        attOper = 0
        for val in numValues:
            for syn in greaterThanSyn:
                tripleCloseness=wordsCloseness(msg,att,syn,val,DictPenalties)
                if tripleCloseness <threshold:
                    if syn=='at least' or syn=='minimum' or syn=='min'  or 'or equal' in syn:
                        attValueOperator[AttributeNum[att]][str(val)]='>='
                    else:
                        attValueOperator[AttributeNum[att]][str(val)]='>'
                    attOper = 1
            for syn in lessThanSyn:
                tripleCloseness = wordsCloseness(msg, att, syn, val,DictPenalties)
                if tripleCloseness < threshold:
                    if syn == 'at most' or syn == 'maximum' or syn == 'max' or 'or equal' in syn:
                        attValueOperator[AttributeNum[att]][str(val)] = '<='
                    else:
                        attValueOperator[AttributeNum[att]][str(val)] = '<'
                    attOper = 1
            for syn in equalSyn:
                tripleCloseness = wordsCloseness(msg, att, syn, val,DictPenalties)
                if tripleCloseness < threshold:
                    attValueOperator[AttributeNum[att]][str(val)] = '='
                    attOper = 1

    # test attribute without operator
        for att in AttributeNum:
            if not AttributeNum[att] in attValueOperator:
                for val in numValues:
                    tripleCloseness = wordsCloseness(msg, att,'', val,DictPenalties2)
                    if tripleCloseness < threshold:
                        attValueOperator[AttributeNum[att]][str(val)] = '='
                        attOper=1
                    if attOper==1:
                        break

    print("dictionary")
    print(attValueOperator)
    print()
    return attValueOperator

def getCountCondition(nodeDetected,numValues,greaterThanSyn,lessThanSyn,equalSyn,msg):
    countValueOperator = defaultdict(dict)
    print(numValues)
    for syn in greaterThanSyn:
        for val in numValues:
            for node in nodeDetected:
                print('ff '+syn+" "+val+" "+node)
                if not nodeDetected[node] in countValueOperator and wordsCloseness(msg,node,syn,val,DictPenalties)<threshold:
                    if syn == 'at least' or syn == 'minimum' or syn == 'min' or 'or equal' in syn:
                        countValueOperator[nodeDetected[node]][str(val)] = '>='
                    else:
                        countValueOperator[nodeDetected[node]][str(val)] = '>'
            if not 'activity' in countValueOperator:
                triple1=wordsCloseness(msg,'contributions',syn,val,DictPenalties)
                triple2=wordsCloseness(msg,'contribution',syn,val,DictPenalties)
                triple3 = wordsCloseness(msg, 'contributed', syn, val,DictPenalties)
                if (not triple1==-1 and triple1<threshold) or (not triple2==-1 and triple2<threshold) or (not triple3==-1 and triple3<threshold):
                    if syn == 'at least' or syn == 'minimum' or syn == 'min' or 'or equal' in syn:
                        countValueOperator['activity'][str(val)] = '>='
                    else:
                        countValueOperator['activity'][str(val)] = '>'

    for syn in lessThanSyn:
        for val in numValues:
            for node in nodeDetected:
                if not nodeDetected[node] in countValueOperator and wordsCloseness(msg,node,syn,val,DictPenalties)<threshold:
                    if syn == 'at most' or syn == 'maximum' or syn == 'max' or 'or equal' in syn:
                        countValueOperator[nodeDetected[node]][str(val)] = '<='
                    else:
                        countValueOperator[nodeDetected[node]][str(val)] = '<'
            if not 'activity' in countValueOperator:
                triple1 = wordsCloseness(msg, 'contributions', syn, val,DictPenalties)
                triple2 = wordsCloseness(msg, 'contribution', syn, val,DictPenalties)
                triple3 = wordsCloseness(msg, 'contributed', syn, val,DictPenalties)
                if (not triple1 == -1 and triple1 < threshold) or (not triple2 == -1 and triple2 < threshold) or (not triple3 == -1 and triple3 < threshold):
                    if syn == 'at most' or syn == 'maximum' or syn == 'max' or 'or equal' in syn:
                        countValueOperator['activity'][str(val)] = '<='
                    else:
                        countValueOperator['activity'][str(val)] = '<'
    for syn in equalSyn:
        for val in numValues:
            for node in nodeDetected:
                if not nodeDetected[node] in countValueOperator and wordsCloseness(msg, node, syn, val,DictPenalties) < threshold:
                    countValueOperator[nodeDetected[node]][str(val)] = '='
            if not 'activity' in countValueOperator:
                triple1 = wordsCloseness(msg, 'contributions', syn, val,DictPenalties)
                triple2 = wordsCloseness(msg, 'contribution', syn, val,DictPenalties)
                triple3 = wordsCloseness(msg, 'contributed', syn, val,DictPenalties)
                if (not triple1 == -1 and triple1 < threshold) or (not triple2 == -1 and triple2 < threshold) or (not triple3 == -1 and triple3 < threshold):
                    countValueOperator['activity'][str(val)] = '='

    #test if there is condition on entity without operator => equal
    for node in nodeDetected:
        if not nodeDetected[node] in countValueOperator:
            for val in numValues:
                triple = wordsCloseness(msg, node, '', val,DictPenalties2)
                if triple<threshold:
                    countValueOperator[nodeDetected[node]][str(val)]='='
                    break
    if not 'activity' in countValueOperator:
        for val in numValues:
            triple1 = wordsCloseness(msg, 'contributions', '', val,DictPenalties2)
            triple2 = wordsCloseness(msg, 'contribution', '', val,DictPenalties2)
            triple3 = wordsCloseness(msg, 'contributed', '', val,DictPenalties2)
            if (not triple1 == -1 and triple1 < threshold) or (not triple2 == -1 and triple2 < threshold) or (not triple3 == -1 and triple3 < threshold):
                countValueOperator['activity'][str(val)] = '='
                break

    print("dictionary2")
    print(countValueOperator)
    print()
    return countValueOperator


def findCategory(intent,resp,entityAttributes,numericalValueOperator,countConditionOperator,nodeDetected,orderByAttribute,orderByCount,msg):
    print()
    print(entityNodes)
    print(entityAttributes)
    print(entityRelation)
    print()

    intent_category=IntentEntitiesInfos.getIntentCategory(intent)

    if(intent_category=='E1'):
        print('E1')
        returned_attributes=IntentEntitiesInfos.getIntentReturned(intent)
        intent_implicitEntities=IntentEntitiesInfos.getIntentImplicitEntities(intent)
        e1Category.activate(nodeNb,entityNodes,entityRelation,entityAttributes,numericalValueOperator,returned_attributes,intent,len(intent_implicitEntities),nodeDetected,aggregationSyn(msg),msg)

    elif intent_category=='E0':
        print('E0')
        returned_node=IntentEntitiesInfos.getIntentReturned(intent) # it should be nodeName or count
        returned_attributes=get_returned_attributes(resp,returned_node[0],entityAttributes,numericalValueOperator) #if returned_node is count then this array will be empty
        e0Category.activate(nodeNb,entityNodes,entityRelation,entityAttributes,numericalValueOperator,countConditionOperator,returned_attributes,intent,nodeDetected,aggregationSyn(msg),orderByAttribute,orderByCount,msg)


    #return nodeRelationDetector.activate(entityNodes,entityRelation,entityAttributes,returned_attributes)

class intentDetector(object):
    def activate(resp,msg):
        global entityNodes
        global entityAttributes
        global entityRelation
        global returned_attributes
        global nodeNb
        global relationNb
        global roleNodeNb
        global actorNodeNb
        global activityNodeNb
        global artifactNodeNb
        global constraints_attribute
        global constraints_value
        entityNodes=[]
        entityAttributes={}
        entityRelation=[]
        returned_attributes=[]
        nodeNb=0
        relationNb=0
        roleNodeNb=0
        actorNodeNb=0
        activityNodeNb=0
        artifactNodeNb=0
        constraints_attribute=[]
        constraints_value=[]
        nodeDetected={}
        relationDetected={}
        nodeAndAttributesDetected = []
        numValues=[]
        AttributeNum={}

        activityTimeCondition = defaultdict(dict)

        start_time = time.time()
        for item in resp['entities']:
            str_item_role=str(item)
            str_item=str_item_role.split(":")[0]
            if(str_item.endswith("Node")):
                # get the word of node detected
                index_item=get_maxConfidence_entities(resp,str_item_role)
                nodeWordDetected=resp['entities'][item][index_item]['value']
                nodeWordDetected=nodeWordDetected.lower()
                nodeAndAttributesDetected.insert(0, nodeWordDetected)
                if(str_item.endswith("ArtifactNode")):
                    #get name of artifact node
                    nodeName=stringExtractor.getName(str_item)
                    nodeDetected[nodeWordDetected]=nodeName
                    if(not nodeName  in entityNodes):
                        entityNodes.insert(0,nodeName)
                        nodeNb=nodeNb+1
                        artifactNodeNb=artifactNodeNb+1
                if(str_item.endswith('activityNode')):
                    nodeDetected[nodeWordDetected]='activity'
                    if(not 'activity'  in entityNodes):
                        entityNodes.insert(0,'activity')
                        nodeNb=nodeNb+1
                        activityNodeNb=activityNodeNb+1
                if(str_item.endswith('actorNode')):
                    nodeDetected[nodeWordDetected]='actor'
                    if(not 'actor' in entityNodes):
                        entityNodes.insert(0,'actor')
                        nodeNb=nodeNb+1
                        actorNodeNb=actorNodeNb+1
                if(str_item.endswith('roleNode')):
                    nodeDetected[nodeWordDetected]='role'
                    if(not 'role'  in entityNodes):
                        entityNodes.insert(0,'role')
                        nodeNb=nodeNb+1
                        roleNodeNb=roleNodeNb+1
                if(str_item.endswith('artifactNode')):
                    nodeDetected[nodeWordDetected]='artifact'
                    if(not 'artifact'  in entityNodes):
                        entityNodes.insert(0,'artifact')
                        nodeNb=nodeNb+1
            elif(str_item.endswith('Relation')):
                index_item=get_maxConfidence_entities(resp,str_item_role)
                relationWordDetected=resp['entities'][item][index_item]['value']
                relationWordDetected=relationWordDetected.lower()
                #if relationWordDetected=='contributions' or relationWordDetected=='contribution':
                    #nodeAndAttributesDetected.insert(0,relationWordDetected)
                relationName=stringExtractor.getRelationName(str_item)
                if not relationName in entityRelation:
                    entityRelation.insert(0,relationName)
                    relationDetected[relationWordDetected]=relationName
                relationNb=relationNb+1
            elif(str_item.endswith("KeyWord")):
                # get the word of attribute detected
                index_item=get_maxConfidence_entities(resp,str_item_role)
                attributeWordDetected=resp['entities'][item][index_item]['value']
                attributeWordDetected=attributeWordDetected.lower() #requested amount
                nodeAndAttributesDetected.insert(0,attributeWordDetected)
                attribute=stringExtractor.getReturnedAttributeName(str_item) #applicationRequestedAmount
                if Dictionary.isNumericalValue(attribute):
                    AttributeNum[attributeWordDetected]=attribute
                nodeExtracted=stringExtractor.getName(attribute)
                if not nodeExtracted in entityNodes:
                    entityNodes.insert(0,nodeExtracted)
                    nodeNb=nodeNb+1
                    if(Dictionary.isArtifactNode(nodeExtracted)==1):
                        artifactNodeNb=artifactNodeNb+1
                    if(Dictionary.isActivityNode(nodeExtracted)==1):
                        activityNodeNb=activityNodeNb+1
                    if(Dictionary.isActorNode(nodeExtracted)==1):
                        actorNodeNb=actorNodeNb+1
                    if(Dictionary.isRoleNode(nodeExtracted)==1):
                        roleNodeNb=roleNodeNb+1
            elif str_item.startswith('wit$number'):
                for numericalItem in resp['entities'][item]:
                    value=numericalItem['value']
                    numValues.insert(0,str(value))
            elif str_item.startswith('wit$datetime'):
                #add activity node
                if (not 'activity' in entityNodes):
                    entityNodes.insert(0, 'activity')
                    nodeNb = nodeNb + 1
                for dateItem in resp['entities'][item]:
                    if dateItem['type']=='interval':
                        dateItem_keys= dateItem.keys()
                        if 'from' in dateItem_keys:
                            activityTimeCondition['activityCompleteTime'][dateItem['from']['value']]='>='
                        if 'to' in dateItem_keys:
                            activityTimeCondition['activityCompleteTime'][dateItem['to']['value']]='<='
                    # only one value
                    else:
                        activityTimeCondition['activityCompleteTime'][dateItem['value']] = '>='

            elif str_item.endswith('Value'):
                attributeName=stringExtractor.getAttributeName(str_item)
                attributeNode=stringExtractor.getName(attributeName)
                index_item=get_maxConfidence_entities(resp,str_item_role)
                if not attributeNode in entityNodes:
                    entityNodes.insert(0,attributeNode)
                    nodeNb=nodeNb+1
                    if(Dictionary.isArtifactNode(attributeNode)==1):
                        artifactNodeNb=artifactNodeNb+1
                    if(Dictionary.isActivityNode(attributeNode)==1):
                        activityNodeNb=activityNodeNb+1
                    if(Dictionary.isActorNode(attributeNode)==1):
                        actorNodeNb=actorNodeNb+1
                    if(Dictionary.isRoleNode(attributeNode)==1):
                        roleNodeNb=roleNodeNb+1
                entityAttributes[attributeName]=resp['entities'][item][index_item]['value']


        intent=resp['intents'][0]['name']
        intent_implicitEntities=IntentEntitiesInfos.getIntentImplicitEntities(intent)
        ### check missing entities
        for item in intent_implicitEntities:
            if item.endswith("Node"):
                if(item.endswith("ArtifactNode")):
                    #get name of artifact node
                    nodeName=stringExtractor.getName(item)
                    if(not nodeName  in entityNodes):
                        entityNodes.insert(0,nodeName)
                        nodeNb=nodeNb+1
                        artifactNodeNb=artifactNodeNb+1
                if(item.endswith('activityNode')):
                    if(not 'activity'  in entityNodes):
                        entityNodes.insert(0,'activity')
                        nodeNb=nodeNb+1
                        activityNodeNb=activityNodeNb+1
                if(item.endswith('actorNode')):
                    if(not 'actor' in entityNodes):
                        entityNodes.insert(0,'actor')
                        nodeNb=nodeNb+1
                        actorNodeNb=actorNodeNb+1
                if(item.endswith('roleNode')):
                    if(not 'role'  in entityNodes):
                        entityNodes.insert(0,'role')
                        nodeNb=nodeNb+1
                        roleNodeNb=roleNodeNb+1
                if(item.endswith('artifactNode')):
                    if(not 'artifact'  in entityNodes):
                        entityNodes.insert(0,'artifact')
                        nodeNb=nodeNb+1
            elif(item.endswith('Relation')):
                relationName=stringExtractor.getRelationName(item)
                if relationName not in entityRelation:
                    entityRelation.insert(0,relationName)
                    relationNb=relationNb+1
        #returned_attributes=get_returned_attributes(resp,entityNodes[0])
        greaterThan=greaterThanSyn(msg)
        lessThan=lessThanSyn(msg)
        equal=equalSyn(msg)
        numericalValueOperator=getAttributeValueOperator(activityTimeCondition,AttributeNum,numValues,greaterThan,lessThan,equal,msg)
        countConditionOperator=getCountCondition(nodeDetected,numValues,greaterThan,lessThan,equal,msg)
        orderByAttribute,orderByCount=getOrderByAttributeOrNode(orderBySyn(msg),nodeAndAttributesDetected,AttributeNum,nodeDetected,msg)
        print("--- %s seconds ---" % (time.time() - start_time))
        return findCategory(intent,resp,entityAttributes,numericalValueOperator,countConditionOperator,nodeDetected,orderByAttribute,orderByCount,msg)

def emptyAllArray():
    global entityNodes
    global entityAttributes
    global entityRelation
    global returned_attributes
    global nodeNb
    global relationNb
    global roleNodeNb
    global actorNodeNb
    global activityNodeNb
    global artifactNodeNb
    global constraints_attribute
    global constraints_value
    entityNodes=[]
    entityAttributes={}
    entityRelation=[]
    returned_attributes=[]
    nodeNb=0
    relationNb=0
    roleNodeNb=0
    actorNodeNb=0
    activityNodeNb=0
    artifactNodeNb=0
    constraints_attribute=[]
    constraints_value=[]





