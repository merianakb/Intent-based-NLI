import time
from collections import defaultdict
from py2neo import Graph

import Category1
import Dictionary
import IntentEntitiesInfos
import QueryConstructor
from NodeRelationDetector import nodeRelationDetector
from StringExtractor import stringExtractor

graph=Graph('bolt://localhost:7687',auth=("neo4j","MyGraphP@ss"))

matchClause=""
whereClause=""
nodeRelation= defaultdict(dict)

def execute_query(query):
    start_time = time.time()
    try:
        data=graph.run(query).to_table()
    except:
        print("Error please repeat the question with another syntax")
        return "Error"
    print("--- %s seconds ---" % (time.time() - start_time))
    printAnswer(data)
    return data


def printAnswer(data):
    for  record in data:
            print (record)

def constructQueryAggFunction(matchclause,whereclause,symb,returnedAttribute,fixedNode):
    nodeName=stringExtractor.getName(returnedAttribute)
    cc=stringExtractor.getFirstAndLastChar(nodeName)
    query="match "+matchclause+" "
    if not whereclause=='':
        query=query+"where "+whereclause+" "
    if not fixedNode=='':
        fl=stringExtractor.getFirstAndLastChar(fixedNode)
        query=query+" WITH "+fl+","+cc
        query=query+" return "+fl+", "+symb+"("+cc+"."+returnedAttribute+")"
    else:
        query=query+" return "+symb+"("+cc+"."+returnedAttribute+")"
    print(query)
    return execute_query(query)


def constructQueryMinMaxWithRelation(matchclause,whereclause,orderBy,returnedNode,intent):
    query="match "+matchclause+" "
    if not whereclause=='':
        query=query+"where  "+whereclause+" "
    cc=stringExtractor.getFirstAndLastChar(returnedNode)
    implicitEntities=IntentEntitiesInfos.getIntentImplicitEntities(intent)
    fixedNode=''
    for item in implicitEntities:
        if item.endswith("Node") and not item.startswith(returnedNode):
            fixedNode=stringExtractor.getName(item)
            break
    fl=stringExtractor.getFirstAndLastChar(fixedNode)

    query=query+"with "+fl+", count(DISTINCT "+cc+") as ct " \
            "order by ct "+orderBy+" limit 1 " \
            "return  ct"
    print(query)
    return execute_query(query)

def constructQueryAggWithRelation(matchclause,whereclause,symb,returnedNode,intent):
    query="match "+matchclause+" "
    if not whereclause=='':
        query=query+"where  "+whereclause+" "
    cc=stringExtractor.getFirstAndLastChar(returnedNode)
    implicitEntities=IntentEntitiesInfos.getIntentImplicitEntities(intent)
    fixedNode=''
    for item in implicitEntities:
        if item.endswith("Node") and not item.startswith(returnedNode):
            fixedNode=stringExtractor.getName(item)
            break
    fl=stringExtractor.getFirstAndLastChar(fixedNode)
    query=query+"with "+fl+", count(DISTINCT "+cc+") as ct " \
            "return  "+symb+"(ct)"
    print(query)
    return execute_query(query)

def getFixedNode(nodeDetected,syn,msg):
    for item in nodeDetected:
        if syn+" "+item in msg:
            return nodeDetected[item]
    return ''

class e1Category(object):
    def activate(nodeNb,entityNodes,entityRelation,entityAttributes,numericalValueOperator,returned_attributes,intent,implicitNodeNB,nodeDetected,aggregationSyn,msg):
        ######get the constructed sub-graph to be selected############
        if nodeNb==1 and len(entityRelation)==0:
            matchClause,whereClause=Category1.constructMatchWhereClause(entityNodes[0].title(),entityAttributes,numericalValueOperator)
        else:
            nodeRelation=nodeRelationDetector.activate(entityNodes,entityRelation)
            matchClause,whereClause=QueryConstructor.constructMatchWhereClause(nodeRelation,entityAttributes,numericalValueOperator)

        if not aggregationSyn=='':
            fixedNode=getFixedNode(nodeDetected,aggregationSyn,msg)
        else:
            fixedNode=''

        if intent.startswith('Max'):
            ### Max of attribute
            if implicitNodeNB==1:
                constructQueryAggFunction(matchClause,whereClause,'MAX', returned_attributes[0],fixedNode)
            ### Max for number of nodes
            else:
                constructQueryAggWithRelation(matchClause,whereClause,'MAX',returned_attributes[0],intent)

        if intent.startswith('Min'):
            ### Min of attribute
            if implicitNodeNB==1:
                constructQueryAggFunction(matchClause,whereClause,'MIN', returned_attributes[0],fixedNode)
            ### Min of number of nodes
            else:
                constructQueryAggWithRelation(matchClause,whereClause,'MIN',returned_attributes[0],intent)

        if intent.startswith('Sum'):
            ### Sum of attribute
            if implicitNodeNB==1:
                constructQueryAggFunction(matchClause,whereClause,'SUM', returned_attributes[0],fixedNode)
            ### Sum of number of nodes
            else:
                constructQueryAggWithRelation(matchClause,whereClause,'SUM',returned_attributes[0],intent)

        if intent.startswith('Avg'):
            ### Avg of attribute
            if implicitNodeNB==1:
                constructQueryAggFunction(matchClause,whereClause,'AVG', returned_attributes[0],fixedNode)
            ### Avg of number of nodes
            else:
                constructQueryAggWithRelation(matchClause,whereClause,'AVG',returned_attributes[0],intent)
