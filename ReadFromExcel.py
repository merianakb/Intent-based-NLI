# Reading an excel file using Python
import xlrd

from py2neo import Graph

graph=Graph('bolt://localhost:7687',auth=("neo4j","MyGraphP@ss"))

def getEmail(s):
    email=""
    i=3
    while i<len(s)-1:
        email=email+s[i]
        i=i+1
    return email

def getBusinessRole(s):
    role=""
    i=3
    while i<len(s)-1:
        role=role+s[i]
        i=i+1
    return role

ActorRole={}
BusinessRole=[]

def getData(indexRow,indexCol):
    if(sheet.cell_value(indexRow,indexCol)=='[]'):
        return
    array=sheet.cell_value(indexRow, indexCol).split(')')
    firstItem=0
    #[('steve.olinde@enron.com', 25, ['specialist', 'trading'])
    for item in array:
        if item ==']':  #last item
            break;
        email=""
        role=""
        oneActor=item.split(",")
        if firstItem==0:
            #[('steve.olinde@enron.com
            email=getEmail(oneActor[0])
            #['specialist'
            if not oneActor[2] == '[]':
                role=getBusinessRole(oneActor[2])
            firstItem=1
        else:
            email=getEmail(oneActor[1])
            if not oneActor[3] == '[]':
                role=getBusinessRole(oneActor[3])

        ActorRole[email]=role
        if(not role=='' and role not in BusinessRole ):
                    BusinessRole.append(role)

# Give the location of the file
loc = ("C:/Users/user/Desktop/Courses/Master2/Stage/MyPapers/chatbot/Marwa Files/resultm__forney.xlsx")

# To open Workbook
wb = xlrd.open_workbook(loc)
sheet = wb.sheet_by_index(0)

#get emails from actRecipients
i=1
while i<sheet.nrows:
    getData(i,6)
    i=i+1

#get emails from actInCC
i=1
while i<sheet.nrows:
    getData(i,7)
    i=i+1

print(ActorRole)
print(BusinessRole)

#create query to insert data in neo4j
''''
for actor in ActorRole:
    query="MERGE (n: Actor {Email: '"+actor+"'})"
    try:
        data=graph.run(query)
    except:
        print("Error1 ")
        print("actor not created "+actor)

    if not ActorRole[actor]=='':
        query2="MERGE (m: Role {Name: '"+ActorRole[actor]+"'})"
        try:
            data=graph.run(query2)
        except:
            print("Error2 ")


        query3="MATCH (n: Actor{Email: '"+actor+"'}),(m: Role {Name: '"+ActorRole[actor]+"'})" \
                "MERGE (n)-[:ActorWithRole]->(m)"
        try:
            data=graph.run(query3)
        except:
            print("Error3 please repeat the question with another syntax")
'''



