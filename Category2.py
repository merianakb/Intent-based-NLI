from py2neo import Graph
from StringExtractor import stringExtractor

graph=Graph('bolt://localhost:7687',auth=("neo4j","MyGraphP@ss"))

constraints_attribute= []
constraints_value= []

class cat2(object):
    def activate(resp,intent_index):
        node_type1=resp['intents'][intent_index]['name'].split('_')[1]
        relation=resp['intents'][intent_index]['name'].split('_')[2]
        node_type2=resp['intents'][intent_index]['name'].split('_')[3]


        constraints_attribute,constraints_value=get_Constraints(resp)
        returned_attribute=get_returned_attributes(resp,node_type1)



        execute_query(node_type1.title(),node_type2.title(),relation,returned_attribute,constraints_attribute,constraints_value)


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

def execute_query(node_type1,node_type2,relation,returned_attribute,constraints_attribute,constraints_value):
    if(len(constraints_attribute)>2):
        return "You can not specify more than 2 constarints"
    returned=""
    i=0
    for item in returned_attribute:
        if(i!=0):
            returned=returned+","
        else:
            i=i+1
        returned=returned+"n."+item
    #pas de constraint
    if(len(constraints_attribute)==0):
        if(len(returned_attribute)==0):
            query="MATCH (n :"+node_type1+")-[:"+relation+"]-(m :"+node_type2+") " \
                "RETURN  (n)"
        else:
            query= "MATCH (n :"+node_type1+")-[:"+relation+"]-(m :"+node_type2+") " \
                "RETURN  "+returned
        print(query)
        print()
        data=graph.run(query).to_table()

    if(len(constraints_attribute)==1):
        if(len(returned_attribute)==0):
            query="MATCH (n:"+node_type1+")-[:"+relation+"]-(m :"+node_type2+") " \
                "WHERE m."+constraints_attribute[0]+"=~ {value0} " \
                "RETURN  (n)"
        else:
            query="MATCH (n:"+node_type1+")-[:"+relation+"]-(m :"+node_type2+") " \
                "WHERE m."+constraints_attribute[0]+"=~ {value0} " \
                "RETURN  "+returned
        print(query)
        print()
        data=graph.run(query,value0='(?i)'+constraints_value[0]).to_table()

    if(len(constraints_attribute)==2):
        if(len(returned_attribute)==0):
            query="MATCH (n:"+node_type1+")-[:"+relation+"]-(m :"+node_type2+")  " \
                "WHERE m."+constraints_attribute[0]+"=~ {value0} AND m."+constraints_attribute[1]+"=~ {value1} " \
                "RETURN  (n)"
        else:
            query="MATCH (n:"+node_type1+")-[:"+relation+"]-(m :"+node_type2+")  " \
                "WHERE m."+constraints_attribute[0]+"=~ {value0} AND " \
                        "m."+constraints_attribute[1]+"=~ {value1} " \
                "RETURN "+returned
        print(query)
        print()
        data=graph.run(query,value0='(?i)'+constraints_value[0],value1='(?i)'+constraints_value[1]).to_table()
    printAnswer(data)
    return data

def printAnswer(data):
    for  record in data:
            print (record)
