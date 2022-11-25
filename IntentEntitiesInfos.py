import json

###########################load intent informations file ######################################
intent_file = json.load(open("C:/Users/HP/Desktop/Courses/PhD/presentation/NourPres/intents.json"))

def getIntentIndex(intent):
    index=0
    for item in intent_file:
        if item['intent']==intent:
            return index
        index=index+1

    return -1

def getIntentCategory(intent):
    intent_index=getIntentIndex(intent)
    intent_category=intent_file[intent_index]['category']
    return intent_category

def getIntentImplicitEntities(intent):
    intent_index=getIntentIndex(intent)
    intent_implicitEntities=intent_file[intent_index]['implicitEntities']
    return intent_implicitEntities

def getIntentReturned(intent):
    intent_index=getIntentIndex(intent)
    intent_return=intent_file[intent_index]['return']
    return intent_return


def getIntentInfos(intent):
    intent_index=getIntentIndex(intent)
    if intent_index==-1:
        return
    intent_infos=intent_file[intent_index]
    print(intent_infos)
    intent_infos_keys=intent_infos.keys()


class intentEntitiesInfos(object):
    def activate (resp):
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
