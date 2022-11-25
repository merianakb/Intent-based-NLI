from py2neo import Graph

import Dictionary
from StringExtractor import stringExtractor

#graph=Graph('bolt://localhost:7687',auth=("neo4j","MyGraphP@ss"))

constraints_attribute= []
constraints_value= []

#class cat1(object):
    #def activate(resp,intent_index):


def get_Constraints(response):
    constraints_attribute= []
    constraints_value= []

    for item in response['entities']:
        str_item=str(item) #positionType:positionType
        if(not str_item.endswith("KeyWord") and not str_item.endswith("Node") and not str_item.endswith("Relation")):
            index_item=get_maxConfidence_entities(response,str_item)
            constraints_attribute.append(str_item.split(':')[0]) #positionType
            constraints_value.append(response['entities'][item][index_item]['value'])
    return constraints_attribute,constraints_value

def get_returned_attributes(response,node):
    returned_attribute=[]
    for item in response['entities']:
        str_item=str(item) #positionType:positionType
        str_item=str_item.split(':')[0]
        if(str_item.endswith("KeyWord") and str_item.startswith(node)):
            att=stringExtractor.getReturnedAttributeName(str_item)
            returned_attribute.append(att)
    return returned_attribute

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

def constructMatchWhereClause(node_type,entityAttribute,numericalValueOperator):
    #construct MATCH clause
    artifactNameConstraint=""
    isartifact=0
    ccA=stringExtractor.getFirstAndLastChar(node_type)
    if Dictionary.isArtifactNode(node_type.lower()):
        s="("+ccA+": Artifact)"
        artifactNameConstraint=artifactNameConstraint+" "+ccA+".Type=~ '(?i)"+node_type+"' "
        isartifact=1
    else:
        s="("+ccA+":"+node_type+")"


    #construct where consitions part
    k=0
    constraints=""
    if(isartifact):
        constraints=artifactNameConstraint
        k=1
    for item in entityAttribute:
        if(k!=0):
            constraints=constraints+" AND "
        else:
            k=k+1
        nodeName=stringExtractor.getName(item)
        cc=stringExtractor.getFirstAndLastChar(nodeName)
        constraints=constraints+" "+cc+"."+item+"=~ '(?i)"+entityAttribute[item]+"' "

    for attribute in numericalValueOperator:
        if(k!=0):
            constraints=constraints+" AND "
        else:
            k=k+1
        G=0
        for value in numericalValueOperator[attribute]:
            if not G == 0 :
                constraints = constraints + " AND "
            nodeName = stringExtractor.getName(attribute)
            cc = stringExtractor.getFirstAndLastChar(nodeName)
            operator = numericalValueOperator[attribute][value]
            if not attribute == 'activityCompleteTime':
                constraints = constraints + " " + cc + "." + attribute + operator + value
                break
            else:
                activity_date_constraint = "datetime(" + cc + "." + attribute + ")"
                value_date_constraint = "datetime('" + value + "')"
                constraints = constraints + " " + activity_date_constraint + operator + value_date_constraint
            if G == 0:
                G = G + 1
    return s,constraints
'''''
def execute_query(node_type,returned_attribute,constraints_attribute,constraints_value):
    #construct MATCH clause
    artifactNameConstraint=""
    isartifact=0
    ccA=stringExtractor.getFirstAndLastChar(node_type)
    if Dictionary.isArtifactNode(node_type.lower()):
        s="("+ccA+": Artifact)"
        artifactNameConstraint=artifactNameConstraint+" "+ccA+".Type=~ '(?i)"+node_type+"' "
        isartifact=1
    else:
        s="("+ccA+":"+node_type+")"

    #construct where consitions part
    k=0
    constraints=""
    if(isartifact):
        constraints=artifactNameConstraint
        k=1
    itemNb=0
    while itemNb<len(constraints_attribute):
        if(k!=0):
            constraints=constraints+" AND "
        else:
            k=k+1
        constraints=constraints+" "+ccA+"."+constraints_attribute[itemNb]+"=~ '(?i)"+constraints_value[itemNb]+"' "
        itemNb=itemNb+1

    #construct RETURN clause
    returned=""
    i=0
    if(len(returned_attribute)==0):
        returned="("+ccA+")"
    else:
        for item in returned_attribute:
            if(i!=0):
                returned=returned+","
            else:
                i=i+1
            returned=returned+ccA+"."+item

    query="MATCH "+s+" " \
            "WHERE "+constraints+" " \
            "RETURN "+returned
    print(query)
    print()
    try:
        data=graph.run(query).to_table()
    except:
        print("Error please repeat the question with another syntax")
        return "Error"
    printAnswer(data)
    return data
    
'''

def printAnswer(data):
    for  record in data:
            print (record[0])




