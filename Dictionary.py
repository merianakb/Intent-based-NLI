from collections import defaultdict

nodes=["Actor","Activity","Artifact"]
artifactNodes=["Workflow","Offer","Application"]
edge= {"Actor":["Actvity"],
       "Activity":["Actor","Offer","Workflow","Application"],
       "Offer":["Activity","Application","Workflow"],
       "Workflow":["Activity","Application","Offer"],
       "Application":["Activity","Offer","Workflow"]}
relationName = defaultdict(dict)

relationName['Actor']['Activity']=['HasExecuted']
relationName['Activity']['Actor']=['HasExecuted']

relationName['Activity']['Activity']=['FollowedBy','ApplicationFollowedBy','OfferFollowedBy','WorkflowFollowedBy']

relationName['Activity']['Artifact']=['AffectArtifact']
relationName['Artifact']['Activity']=['AffectArtifact']

relationName['Activity']['Application']=['AffectArtifact']
relationName['Application']['Activity']=['AffectArtifact']

relationName['Activity']['Offer']=['AffectArtifact']
relationName['Offer']['Activity']=['AffectArtifact']

relationName['Activity']['Workflow']=['AffectArtifact']
relationName['Workflow']['Activity']=['AffectArtifact']

#relation between artifact
relationName['Offer']['Application']=['Offered','CanceledOffer']
relationName['Application']['Offer']=['Offered','CanceledOffer']

relationName['Workflow']['Application']=['WorkOf']
relationName['Application']['Workflow']=['WorkOf']

numericalValues=['applicationRequestedAmount','offerOfferedAmount','offerFirstWithdrawalAmount','offerNumberOfTerms',
                 'offerMonthlyCost']

def getRelationBetweenTwoNodes(node1,node2):
    return relationName[node1][node2]

def getNodesHavingRelationWith(node):
    for item in edge:
        if item==node:
            return edge[item]
    return []

def getDestinationNode(node,relation):
    keyA=node
    for keyB in relationName[keyA]:
        if(relation in relationName[keyA][keyB]):
            return keyB
    return ""

def ifRelationExist(node1,node2):
    keyA=node1
    keyB=node2
    if (keyA in relationName) & (keyB in relationName[keyA]):
        return 1
    return 0

def RelationExist(node1,node2,relation):
     keyA=node1
     keyB=node2
     relations=relationName[keyA][keyB]
     if(relation in relations):
         return 1
     return 0

def getNodesOfRelation(relation):
    for keyA in relationName:
        for keyB in relationName[keyA]:
            if(relation in relationName[keyA][keyB] ):
                return keyA,keyB
    return "",""

def getImplicitNodes(nodes):
    nodesT=nodes
    if 'role' in nodesT and ('application' in nodesT or 'workflow' in nodesT or 'offer' in nodesT):
        if not 'actor' in nodesT:
            nodesT.append('actor')
        if not 'activity' in nodesT:
            nodesT.append('activity')
    if 'role' in nodesT and 'activity' in nodesT:
        if not 'actor' in nodesT:
            nodesT.append('actor')
    if 'actor' in nodesT and ('application' in nodesT or 'workflow' in nodesT or 'offer' in nodesT):
        if not 'activity' in nodesT:
            nodesT.append('activity')
    return nodesT

def isNumericalValue(s):
    if s in numericalValues:
        return 1
    return 0

def isArtifactNode(s):
    if(s=='offer' or s=='workflow' or s=='application'):
        return 1
    return 0
def isRoleNode(s):
    if(s=='role'):
        return 1
    return 0
def isActorNode(s):
    if(s=='actor'):
        return 1
    return 0
def isActivityNode(s):
    if(s=='activity'):
        return 1
    return 0







