from collections import defaultdict

import Dictionary
from QueryConstructor import queryConstructor

entityNodes=[]
entityAttributes={}
entityRelation=[]
returned_attributes=[]
nodeNb=0
relationNb=0

nodeRelation= defaultdict(dict)
optionalMatch=defaultdict(dict)

class nodeRelationDetector(object):
    def activate(nodes,relations):
        queue_node=[]
        entityRelation=relations
        nodeRelation= defaultdict(dict)
        optionalMatch=defaultdict(dict)

        entityNodes=Dictionary.getImplicitNodes(nodes)

        for item1 in entityNodes:
                item1=item1.title()
                queue_node.append(item1)
                for item2 in entityNodes:
                    item2=item2.title()
                    if(not item1==item2 and not item2 in queue_node):

                        if(Dictionary.ifRelationExist(item1,item2)):

                            find=0
                            for rel in entityRelation:
                                if(Dictionary.RelationExist(item1,item2,rel)):
                                    nodeRelation[item1][item2]=rel
                                    entityRelation.remove(rel)
                                    find=1
                                    break
                            if(find==0): #we should find the relation from dictionary
                                relation=Dictionary.getRelationBetweenTwoNodes(item1,item2)
                                nodeRelation[item1][item2]=relation[0]
        if(len(entityRelation)>0): #we should find implicit nodes
            for item in entityRelation:
                node1,node2=Dictionary.getNodesOfRelation(item)
                if (not node1=="" and not node2=="" ):

                    nodeRelation[node1][node2]=item

                    #we should find relation between node2 and other node extracted
                    for n in entityNodes:
                        if(not n.title()==node1):
                            if(Dictionary.ifRelationExist(n.title(),node2)):
                                relation=Dictionary.getRelationBetweenTwoNodes(n.title(),node2)
                                nodeRelation[n.title()][node2]=relation[0]

                    #we should find relation between node1 and other node extracted
                    for n in entityNodes:
                        if(not n.title()==node2):
                            if(Dictionary.ifRelationExist(n.title(),node1)):
                                relation=Dictionary.getRelationBetweenTwoNodes(n.title(),node1)
                                nodeRelation[n.title()][node1]=relation[0]


        return nodeRelation
        #return queryConstructor.activate(nodeRelation,optionalMatch,entityAttributes,returned_attribute,entityNodes[0])
    #activate(['Role','Actor','Interview','Candidate'],['HasExecuted'],[],[])

