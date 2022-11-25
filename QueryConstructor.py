from collections import defaultdict
from py2neo import Graph

import Dictionary
from StringExtractor import stringExtractor

''''
graph=Graph('bolt://localhost:7687',auth=("neo4j","MyGraphP@ss"))

def execute_query(s,optional,constraints,returned):

   if(not optional==''):
        query="MATCH "+s+" " \
            "WHERE "+constraints+" " \
            "OPTIONAL MATCH "+optional+" " \
            "RETURN "+returned
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
            print (record)

def constructMatchWhereClause(nodeRelation,entityAttribute,numericalValueOperator):
        i=0
        #construct Match part
        query_node=[]
        s=""
        artifactNameConstraint=""
        firstartifact=0
        for  kA in nodeRelation:
            if(i==0):
                i=i+1
            else:
                s=s+","
            ccA=stringExtractor.getFirstAndLastChar(kA)
            if not kA in query_node:
                if Dictionary.isArtifactNode(kA.lower()):
                    s=s+"("+ccA+": Artifact)"
                    if firstartifact==0:
                        firstartifact=1
                    else:
                        artifactNameConstraint=artifactNameConstraint+" AND "
                    artifactNameConstraint=artifactNameConstraint+" "+ccA+".Type=~ '(?i)"+kA+"' "
                else:
                    s=s+"("+ccA+":"+kA+")"
                query_node.append(kA)
            else:
                s=s+"("+ccA+")"
            first=1
            for kB in nodeRelation[kA]:
                if first==1:
                    ccB=stringExtractor.getFirstAndLastChar(kB)
                    relation=nodeRelation[kA][kB]
                    if relation=='AffectArtifact':
                        relation="relTo"+ccB
                        s=s+"-[:AffectArtifact]-"
                    else:
                        s=s+"-[:"+relation+"]-"

                    if not kB in query_node:
                        if Dictionary.isArtifactNode(kB.lower()):
                            s=s+"("+ccB+": Artifact)"
                            if firstartifact==0:
                                firstartifact=1
                            else:
                                artifactNameConstraint=artifactNameConstraint+" AND "
                            artifactNameConstraint=artifactNameConstraint+" "+ccB+".Type=~ '(?i)"+kB+"' "
                        else:
                            s=s+"("+ccB+":"+kB+")"
                        query_node.append(kB)
                    else:
                        s=s+"("+ccB+")"
                    first=0

                else:
                    s=s+",("+ccA+")"
                    ccB=stringExtractor.getFirstAndLastChar(kB)
                    relation=nodeRelation[kA][kB]
                    if relation=='AffectArtifact':
                        #relation="relTo"+ccB
                        s=s+"-[:AffectArtifact]-"
                    else:
                        s=s+"-[:"+relation+"]-"
                    if not kB in query_node:
                        if Dictionary.isArtifactNode(kB.lower()):
                            s=s+"("+ccB+": Artifact)"
                            if firstartifact==0:
                                firstartifact=1
                            else:
                                artifactNameConstraint=artifactNameConstraint+" AND "
                            artifactNameConstraint=artifactNameConstraint+" "+ccB+".Type=~ '(?i)"+kB+"' "
                        else:
                            s=s+"("+ccB+":"+kB+")"
                        query_node.append(kB)
                    else:
                        s=s+"("+ccB+")"
        #construct where consitions part
        k=0
        constraints=""
        if(not artifactNameConstraint==''):
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
                if not G==0 :
                    constraints = constraints + " AND "
                nodeName=stringExtractor.getName(attribute)
                cc=stringExtractor.getFirstAndLastChar(nodeName)
                operator=numericalValueOperator[attribute][value]
                if not attribute == 'activityCompleteTime':
                    constraints = constraints + " " + cc + "." + attribute + operator + value
                    break
                else:
                    activity_date_constraint="datetime("+cc + "." + attribute +")"
                    value_date_constraint="datetime('"+value+"')"
                    constraints=constraints+" "+activity_date_constraint + operator+ value_date_constraint
                if G==0:
                    G=G+1

        return s,constraints



class queryConstructor(object):
    def activate(nodeRelation,optionalMatch,entityAttribute,returned_attributes,firstNode):
        global s
        global optional
        global constraints
        global returned


        s=""
        optional=""
        constraints=""
        returned=""
        returned_attributes=returned_attributes
        entityAttribute=entityAttribute


        i=0
        #construct Match part
        query_node=[]
        s=""
        artifactNameConstraint=""
        firstartifact=0
        for  kA in nodeRelation:
            if(i==0):
                i=i+1
            else:
                s=s+","
            ccA=stringExtractor.getFirstAndLastChar(kA)
            if not kA in query_node:
                if Dictionary.isArtifactNode(kA.lower()):
                    s=s+"("+ccA+": Artifact)"
                    if firstartifact==0:
                        firstartifact=1
                    else:
                        artifactNameConstraint=artifactNameConstraint+" AND "
                    artifactNameConstraint=artifactNameConstraint+" "+ccA+".Type=~ '(?i)"+kA+"' "
                else:
                    s=s+"("+ccA+":"+kA+")"
                query_node.append(kA)
            else:
                s=s+"("+ccA+")"
            first=1
            for kB in nodeRelation[kA]:
                if first==1:
                    ccB=stringExtractor.getFirstAndLastChar(kB)
                    relation=nodeRelation[kA][kB]
                    if relation=='AffectArtifact':
                        relation="relTo"+ccB
                        s=s+"-["+relation+"]-"
                    else:
                        s=s+"-[:"+relation+"]-"

                    if not kB in query_node:
                        if Dictionary.isArtifactNode(kB.lower()):
                            s=s+"("+ccB+": Artifact)"
                            if firstartifact==0:
                                firstartifact=1
                            else:
                                artifactNameConstraint=artifactNameConstraint+" AND "
                            artifactNameConstraint=artifactNameConstraint+" "+ccB+".Type=~ '(?i)"+kB+"' "
                        else:
                            s=s+"("+ccB+":"+kB+")"
                        query_node.append(kB)
                    else:
                        s=s+"("+ccB+")"
                    first=0

                else:
                    s=s+",("+ccA+")"
                    ccB=stringExtractor.getFirstAndLastChar(kB)
                    relation=nodeRelation[kA][kB]
                    if relation=='AffectArtifact':
                        relation="relTo"+ccB
                        s=s+"-["+relation+"]-"
                    else:
                        s=s+"-[:"+relation+"]-"
                    if not kB in query_node:
                        if Dictionary.isArtifactNode(kB.lower()):
                            s=s+"("+ccB+": Artifact)"
                            if firstartifact==0:
                                firstartifact=1
                            else:
                                artifactNameConstraint=artifactNameConstraint+" AND "
                            artifactNameConstraint=artifactNameConstraint+" "+ccB+".Type=~ '(?i)"+kB+"' "
                        else:
                            s=s+"("+ccB+":"+kB+")"
                        query_node.append(kB)
                    else:
                        s=s+"("+ccB+")"
        print()

        #construct where consitions part
        k=0
        constraints=""
        if(not artifactNameConstraint==''):
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

        #construct Return part
        returned=""
        if(len(returned_attributes)==0):
            nodeName=stringExtractor.getName(firstNode)
            cc=stringExtractor.getFirstAndLastChar(nodeName)
            returned="("+cc+")"
        else:
            j=0
            for item in returned_attributes:
                if(j!=0):
                    returned=returned+","
                else:
                    j=j+1
                nodeName=stringExtractor.getName(item)
                cc=stringExtractor.getFirstAndLastChar(nodeName)
                returned=returned+cc+"."+item+""

        return s,constraints
        #return execute_query(s,optional,constraints,returned)


