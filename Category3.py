from py2neo import Graph
from StringExtractor import stringExtractor
graph=Graph('bolt://localhost:7687',auth=("neo4j","MyGraphP@ss"))

constraints_attribute1= []
constraints_value1= []

constraints_attribute2= []
constraints_value2= []

class cat3(object):
    def activate(resp,intent_index):
        node_type1=resp['intents'][intent_index]['name'].split('_')[1]
        node_type2=resp['intents'][intent_index]['name'].split('_')[2]
        node_type3=resp['intents'][intent_index]['name'].split('_')[3]


        constraints_attribute1,constraints_value1,constraints_attribute2,constraints_value2=get_Constraints(resp,node_type2,node_type3)
        returned_attribute=get_returned_attributes(resp,node_type1)
        print(constraints_attribute1)
        print(constraints_value1)
        print(constraints_attribute2)
        print(constraints_value2)

        execute_query(node_type1.title(),node_type2.title(),node_type3.title(),returned_attribute,constraints_attribute1,constraints_value1,
                      constraints_attribute2,constraints_value2)

def get_Constraints(response,node_type2,node_type3):
    constraints_attribute1= []
    constraints_value1= []

    constraints_attribute2= []
    constraints_value2= []

    for item in response['entities']:
        str_item=str(item) #positionType:positionType
        if(not str_item.endswith("KeyWord") and not str_item.endswith("Node") and not str_item.endswith("Relation")):
            index_item=get_maxConfidence_entities(response,str_item)
            itemName=str_item.split(':')[0] #positionType
            if(itemName.startswith(node_type2)): #start with position or candidate...
                constraints_attribute1.append(itemName) #positionType
                constraints_value1.append(response['entities'][item][index_item]['value'])
            elif(itemName.startswith(node_type3)):
                constraints_attribute2.append(itemName)
                constraints_value2.append(response['entities'][item][index_item]['value'])
    return constraints_attribute1,constraints_value1,constraints_attribute2,constraints_value2

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

def execute_query(node_type1,node_type2,node_type3,returned_attribute,constraints_attribute1,constraints_value1,
                  constraints_attribute2,constraints_value2):

    #construct MATCH clause
    ccA=stringExtractor.getFirstAndLastChar(node_type1)
    ccB=stringExtractor.getFirstAndLastChar(node_type2)
    ccC=stringExtractor.getFirstAndLastChar(node_type3)

    s="("+ccA+" :Artifact)-[r]-(a :Activity), " \
                    "(a)-[l]-("+ccB+":Artifact), " \
                    "(a)-[s]-("+ccC+" :Artifact)"

    #construct WHERE clause
    constraints=ccA+".Type=~ '(?i)"+node_type1+"' AND "+ccB+".Type=~ '(?i)"+node_type2+"' " \
               " AND "+ccC+".Type=~ '(?i)"+node_type3+"' "
    itemNb=0
    while itemNb<len(constraints_attribute1):
      constraints=constraints+" AND "
      constraints=constraints+" "+ccB+"."+constraints_attribute1[itemNb]+"=~ '(?i)"+constraints_value1[itemNb]+"' "
      itemNb=itemNb+1

    itemNb=0
    while itemNb<len(constraints_attribute2):
      constraints=constraints+" AND "
      constraints=constraints+" "+ccC+"."+constraints_attribute2[itemNb]+"=~ '(?i)"+constraints_value2[itemNb]+"' "
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

def printAnswer(data):
    for  record in data:
            print (record[0])
