import time

import Category1
import IntentDetector
import IntentEntitiesInfos
import QueryConstructor
from NodeRelationDetector import nodeRelationDetector
from StringExtractor import stringExtractor
from py2neo import Graph

graph=Graph('bolt://localhost:7687',auth=("neo4j","MyGraphP@ss"))

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

def createConditionCount(countConditionOperator):
    whereClause=''
    withClause=''
    countVariable=[]
    first=0
    for item in countConditionOperator:
        if first==0:
            withClause=withClause+""
            whereClause=whereClause+"WHERE "
            first=first+1
        else:
            withClause=withClause+","
            whereClause=whereClause+" AND "
        if item=='*':
            withClause=withClause+" count(*) as ct "
            countVariable.append('*')
        else:
            cc=stringExtractor.getFirstAndLastChar(item)
            withClause=withClause+" count(DISTINCT "+cc+") as "+cc+"Ct "
            countVariable.append(cc)
        for value in countConditionOperator[item]:
            if item=='*':
                whereClause=whereClause+" ct"+countConditionOperator[item][value]+value
            else:
                cc=stringExtractor.getFirstAndLastChar(item)
                whereClause=whereClause+" "+cc+"Ct"+countConditionOperator[item][value]+value
            break
    return withClause,whereClause,countVariable


def constructQueryRelationCount(matchClause,whereClause):
    query="match "+matchClause+" "
    if not whereClause=='':
        query=query+" where "+whereClause
    returnClause=" return count(*)"
    query=query+returnClause
    print(query)
    return execute_query(query)

def contructQueryNodeCount(matchClause,whereClause,nodeName,countConditionOperator,intent):
    query="MATCH "+matchClause+" \n"
    if not whereClause=='':
        query=query+"WHERE "+whereClause
    cc=stringExtractor.getFirstAndLastChar(nodeName)
    withClause,where,countVariable=createConditionCount(countConditionOperator)
    if not withClause=='':
        withClause="WITH "+withClause

    if intent=='Contribution_count':
        if not len(countVariable)==0 and '*' in countVariable:
            returnClause="RETURN ct"
        else:
            returnClause="RETURN count(*)"

    else:
        if not len(countVariable)==0:
            if not cc in countVariable:
                if withClause=='':
                    withClause="WITH "+cc
                else:
                    withClause=withClause+","+cc
        returnClause="RETURN count(DISTINCT "+cc+")"
    if not withClause=='':
        query=query+'\n'+withClause
    if not where=='':
        query=query+'\n'+where
    query=query+'\n'+returnClause
    print(query)
    return execute_query(query)

def constructQueryCountAgg(matchclause,whereclause,nodeName,countConditionOperator,fixedNode,orderByAttribute,orderByCount,orderBySymb,intent):
    query="MATCH "+matchclause+" \n"
    if not whereclause=='':
        query=query+"WHERE  "+whereclause
    fl=stringExtractor.getFirstAndLastChar(fixedNode)
    withclause,where,countVariable=createConditionCount(countConditionOperator)
    withVariable=[]

    withClause="WITH "+fl
    withVariable.append(fl)
    #we have condition count
    if not withclause=='':
        withClause=withClause+","+withclause
        withVariable.append(fl)

    returnClause='RETURN '
    if intent=='Contribution_count':
        if not '*' in countVariable:
            withClause=withClause+",count(*) as ct"
            countVariable.append('*')
        returnClause=returnClause+"("+fl+"),ct"
    else:
        cc=stringExtractor.getFirstAndLastChar(nodeName)
        if not cc in countVariable:
            withClause=withClause+","+cc
            countVariable.append(cc)
        returnClause=returnClause+"("+fl+"),count(DISTINCT "+cc+")"

    orderClause=''
    if not orderByAttribute=='':
        orderClause="ORDER BY "
        node=stringExtractor.getName(orderByAttribute)
        cc=stringExtractor.getFirstAndLastChar(node)
        if not cc in withVariable:
            withClause=withClause+","+cc
            withVariable.append(cc)
        orderClause=orderClause+" "+cc+"."+orderByAttribute+" "+orderBySymb

    elif not orderByCount=='':
        orderClause="ORDER BY "
        orderByNode=orderByCount
        node=stringExtractor.getName(orderByNode)
        variableName=stringExtractor.getFirstAndLastChar(node)
        if not variableName in countVariable:
            withClause=withClause+", count(DISTINCT "+variableName+") as "+variableName+"Ct"
            countVariable.append(variableName)
        orderClause=orderClause+" "+variableName+"Ct "+orderBySymb

    if not withClause=='':
        query=query+'\n'+withClause
    if not where=='':
        query=query+'\n'+where
    if not orderClause=='' and not orderByAttribute=='':
        query=query+'\n'+returnClause
        query=query+'\n'+orderClause
    else:
        if not orderClause=='':
            query = query + '\n' + orderClause
        query=query+'\n'+returnClause

    print(query)
    return execute_query(query)

def constructQueryNode(matchClause,whereClause,nodeName,countConditionOperator,returned_attributes,orderByAttribute,orderByCount,orderBySymb):
    query="MATCH "+matchClause+"\n"
    if not whereClause=='':
        query=query+"WHERE "+whereClause
    withClause,where,countVariable=createConditionCount(countConditionOperator)
    if withClause=='':
        firstWith=1
    else:
        firstWith=0
    withClause="WITH "+withClause
    withVariable=[]

    orderClause=''
    if not orderByAttribute=='':
        orderClause="ORDER BY "
        node=stringExtractor.getName(orderByAttribute)
        cc=stringExtractor.getFirstAndLastChar(node)
        if not cc in withVariable:
            if firstWith==1:
                withClause=withClause+cc
                firstWith=0
            else:
                withClause=withClause+","+cc
            withVariable.append(cc)
        orderClause=orderClause+" "+cc+"."+orderByAttribute+" "+orderBySymb

    elif not orderByCount=='':
        orderClause="ORDER BY "
        orderByNode=orderByCount
        node=stringExtractor.getName(orderByNode)
        variableName=stringExtractor.getFirstAndLastChar(node)
        if not variableName in countVariable:
            if firstWith==1:
                withClause=withClause+" count(DISTINCT "+variableName+") as "+variableName+"Ct"
                firstWith=0
            else:
                withClause=withClause+" count(DISTINCT "+variableName+") as "+variableName+"Ct"
            countVariable.append(variableName)
        orderClause=orderClause+" "+variableName+"Ct "+orderBySymb

    returnClause="RETURN DISTINCT "
    cc=stringExtractor.getFirstAndLastChar(nodeName)
    if not cc in withVariable:
        if firstWith==1:
            withClause=withClause+cc
        else:
            withClause=withClause+","+cc
        withVariable.append(cc)

    #if returned attributes contains only the attribute of order by then we should return the entire node
    if len(returned_attributes)==1 and orderByAttribute in returned_attributes:
        returned_attributes=[]

    if(len(returned_attributes)==0):
        returnClause=returnClause+" ("+cc+")"
    else:
        j=0
        for item in returned_attributes:
            if(j==0):
                returnClause=returnClause+cc+"."+item+""
                j=j+1
            else:
                returnClause=returnClause+","+cc+"."+item+""

    if not withClause=='':
        query=query+'\n'+withClause
    if not where=='':
        query=query+'\n'+where
    if not orderClause == '' and not orderByAttribute == '':
        query = query + '\n' + returnClause
        query = query + '\n' + orderClause
    else:
        if not orderClause == '':
            query = query + '\n' + orderClause
        query = query + '\n' + returnClause

    print(query)
    return execute_query(query)

def constructQueryNodeWithFixedNode(matchClause,whereClause,nodeName,countConditionOperator,fixedNode,returned_attributes,orderByAttribute,orderByCount,orderBySymb):
    query="MATCH "+matchClause+" \n"
    if not whereClause=='':
        query=query+"WHERE  "+whereClause
    fl=stringExtractor.getFirstAndLastChar(fixedNode)
    withclause,where,countVariable=createConditionCount(countConditionOperator)
    withVariable=[]

    withClause="WITH "+fl
    withVariable.append(fl)
    #we have condition count
    if not withclause=='':
        withClause=withClause+","+withclause
        withVariable.append(fl)


    orderClause=''
    if not orderByAttribute=='':
        orderClause="ORDER BY "
        node=stringExtractor.getName(orderByAttribute)
        cc=stringExtractor.getFirstAndLastChar(node)
        if not cc in withVariable:
            withClause=withClause+","+cc
            withVariable.append(cc)
        orderClause=orderClause+" "+cc+"."+orderByAttribute+" "+orderBySymb

    elif not orderByCount=='':
        orderClause="ORDER BY "
        orderByNode=orderByCount
        node=stringExtractor.getName(orderByNode)
        variableName=stringExtractor.getFirstAndLastChar(node)
        if not variableName in countVariable:
            withClause=withClause+", count(DISTINCT "+variableName+") as "+variableName+"Ct"
            countVariable.append(variableName)
        orderClause=orderClause+" "+variableName+"Ct "+orderBySymb

    returnClause="RETURN DISTINCT ("+fl+"),"
    cc=stringExtractor.getFirstAndLastChar(nodeName)
    if not cc in withVariable:
            withClause=withClause+","+cc
            withVariable.append(cc)

    #if returned attributes contains only the attribute of order by then we should return the entire node
    if len(returned_attributes)==1 and orderByAttribute in returned_attributes:
        returned_attributes=[]

    if(len(returned_attributes)==0):
        returnClause=returnClause+" ("+cc+")"
    else:
        j=0
        for item in returned_attributes:
            if(j==0):
                returnClause=returnClause+cc+"."+item+""
                j=j+1
            else:
                returnClause=returnClause+","+cc+"."+item+""

    if not withClause=='':
        query=query+'\n'+withClause
    if not where=='':
        query=query+'\n'+where
    if not orderClause == '' and not orderByAttribute == '':
        query = query + '\n' + returnClause
        query = query + '\n' + orderClause
    else:
        if not orderClause == '':
            query = query + '\n' + orderClause
        query = query + '\n' + returnClause

    print(query)
    return execute_query(query)

def getFixedNode(nodeDetected,syn,msg):
    for item in nodeDetected:
        if syn+" "+item in msg:
            return nodeDetected[item]
    return ''

class e0Category(object):
    def activate(nodeNb,entityNodes,entityRelation,entityAttributes,numericalValueOperator,countConditionOperator,returned_attributes,intent,nodeDetected,aggregationSyn,orderByAttribute,orderByCount,msg):
        ######get the constructed sub-graph to be selected############
        if nodeNb==1 and len(entityRelation)==0:
            matchClause,whereClause=Category1.constructMatchWhereClause(entityNodes[0].title(),entityAttributes,numericalValueOperator)

        else:
            nodeRelation=nodeRelationDetector.activate(entityNodes,entityRelation)
            matchClause,whereClause=QueryConstructor.constructMatchWhereClause(nodeRelation,entityAttributes,numericalValueOperator)

        ## Node.count or Node.Relation.count
        if intent.endswith('count'):
            nodeName=stringExtractor.getNodeNameFromIntent(intent)
            # count with agg
            if not aggregationSyn=='':
                fixedNode=getFixedNode(nodeDetected,aggregationSyn,msg)
                if fixedNode=='':
                    print('To return aggregation count you should specify the fixed node')
                    return
                orderBySymb='ASC'
                if not IntentDetector.DESCSymbSyn(msg)=='':
                    orderBySymb='DESC'
                constructQueryCountAgg(matchClause,whereClause,nodeName.lower(),countConditionOperator,fixedNode,orderByAttribute,orderByCount,orderBySymb,intent)
            else:
                contructQueryNodeCount(matchClause,whereClause,nodeName.lower(),countConditionOperator,intent)

        ## Node or Node.Relation
        else:
            nodeName=stringExtractor.getNodeNameFromIntent(intent)
            orderBYSymb='ASC'
            if not IntentDetector.DESCSymbSyn(msg)=='':
                orderBYSymb='DESC'
            if not aggregationSyn=='':
                fixedNode=getFixedNode(nodeDetected,aggregationSyn,msg)
                if not fixedNode=='':
                    constructQueryNodeWithFixedNode(matchClause,whereClause,nodeName.lower(),countConditionOperator,fixedNode,returned_attributes,orderByAttribute,orderByCount,orderBYSymb)
                else:
                    constructQueryNode(matchClause,whereClause,nodeName.lower(),countConditionOperator,returned_attributes,orderByAttribute,orderByCount,orderBYSymb)
            else:
                constructQueryNode(matchClause,whereClause,nodeName.lower(),countConditionOperator,returned_attributes,orderByAttribute,orderByCount,orderBYSymb)
