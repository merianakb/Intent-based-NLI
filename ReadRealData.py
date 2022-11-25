import xlrd

from py2neo import Graph
from datetime import datetime
import time

start_time = time.time()

activity_list=[]
actor_list=[]
application_list=[]
offer_list=[]
workflow_list=[]

def floatHourToTime(fh):
    h, r = divmod(fh, 1)
    m, r = divmod(r*60, 1)
    return (
        int(h),
        int(m),
        int(r*60),
    )

graph=Graph('bolt://localhost:7687',auth=("neo4j","MyGraphP@ss"))

# Give the location of the file
loc = ("BPI Challenge 2017 (filtered2).xlsx")


# To open Workbook
wb = xlrd.open_workbook(loc)
sheet = wb.sheet_by_index(0)

i=1
print(sheet.nrows)
while i<sheet.nrows:
    activity_id=str(i)
    activity_name=sheet.cell_value(i,1)
    activity_startTime=sheet.cell_value(i,2)
    activity_startTime_date=datetime(*xlrd.xldate_as_tuple(activity_startTime, wb.datemode))
    activity_startTime_date=str(activity_startTime_date).replace(" ","T",1)
    activity_completeTime=sheet.cell_value(i,3)
    activity_completeTime_date=datetime(*xlrd.xldate_as_tuple(activity_completeTime, wb.datemode))
    activity_completeTime_date=str(activity_completeTime_date).replace(" ","T",1)

    #print("activityname: "+activity_name+" /startTime: "+activity_startTime+" /completeTime: "+activity_completeTime+" /actor:  "+actor_name)
    if activity_name not in activity_list:
        activity_list.append(activity_name)
    #create activity node
    query="CREATE (n: Activity {ID: '"+activity_id+"' ,activityName: '"+activity_name+"',activityStartTime: '"+str(activity_startTime_date)+"' ," \
                                "activityCompleteTime: '"+str(activity_completeTime_date)+"'})"
    try:
        data=graph.run(query)
    except:
        print("activity not created "+activity_name)
    print("Activity created "+activity_name)

    actor_name=sheet.cell_value(i,12)
    if actor_name not in actor_list:
        actor_list.append(actor_name)
        #Create Actor node
        query2="CREATE (m: Actor {actorName: '"+actor_name+"'})"
        try:
            data=graph.run(query2)
        except:
            print("actor not created "+actor_name)
        print("Actor created "+actor_name)

    #Create Relation between actor and activity
    query3="MATCH (n: Actor{actorName: '"+actor_name+"'}),(m: Activity { ID:'"+activity_id+"'})" \
                "MERGE (n)-[:HasExecuted]->(m)"
    try:
        data=graph.run(query3)
    except:
        print("Error on creation relation")

    event_origin=sheet.cell_value(i,14)

    #Application Artifact
    application_id=sheet.cell_value(i,0)
    application_loanGoal=sheet.cell_value(i,4)
    application_type=sheet.cell_value(i,5)
    application_requestedAmount=str(sheet.cell_value(i,6))
    #print("application id: "+application_id+" \ loan goal: "+application_loanGoal+" \ type: "+application_type+" \ amount: "+application_requestedAmount)
    if application_id not in application_list:
        application_list.append(application_id)
        #Create Application node
        query2="CREATE (m: Artifact:Application {Type: 'Application', applicationID: '"+application_id+"', applicationLoanGoal: '"+application_loanGoal+"', applicationType: '"+application_type+"', applicationRequestedAmount: "+str(application_requestedAmount)+"})"
        try:
            data=graph.run(query2)
        except:
            print("application not created "+application_id)
        print("Application Created: "+application_id)

    #Create Relation between Application and Activity
    query3="MATCH (n: Artifact:Application{Type: 'Application', applicationID: '"+application_id+"'}),(m: Activity { ID:'"+activity_id+"'})" \
                "MERGE (m)-[:AffectArtifact]->(n)"
    try:
        data=graph.run(query3)
    except:
        print("Error on creation relation")

    if event_origin=='Offer':
        #Offer Artifact
        offerID=sheet.cell_value(i,11)
        offerID2=sheet.cell_value(i,15)
        if offerID2.startswith('Offer_'):
            offer_id=sheet.cell_value(i,15)
        else:
            offer_id=offerID
        offer_firstWithdrawalAmount=str(sheet.cell_value(i,8))
        offer_numberOfTerms=str(sheet.cell_value(i,9))
        offer_monthlyCost=str(sheet.cell_value(i,13))
        offer_CreditScore=str(sheet.cell_value(i,17))
        offer_offeredAmount=str(sheet.cell_value(i,18))
        #print("offer id: "+offer_id+" \ first: "+offer_firstWithdrawalAmount+" \ monthlycost: "+offer_monthlyCost+
              #" \ amount: "+offer_offeredAmount+" \ credit: "+offer_CreditScore+" \ terms: "+offer_numberOfTerms)
        if offer_id not in offer_list:
            offer_list.append(offer_id)
            #Create Offer node
            query2="CREATE (m: Artifact:Offer {Type: 'Offer', offerID: '"+offer_id+"', offerFirstWithdrawalAmount: "+str(offer_firstWithdrawalAmount)+", offerNumberOfTerms: "+str(offer_numberOfTerms)+", offerMonthlyCost: "+str(offer_monthlyCost)+", offerCreditScore: "+str(offer_CreditScore)+", offerOfferedAmount: "+str(offer_offeredAmount)+"})"
            try:
                data=graph.run(query2)
            except:
                print("offer not created "+offer_id)
            print("Offer Created: "+offer_id)

        #Create Relation between Offer and Activity
        query3="MATCH (n: Artifact:Offer{Type: 'Offer', offerID: '"+offer_id+"'}),(m: Activity { ID:'"+activity_id+"'})" \
                "MERGE (m)-[:AffectArtifact]->(n)"
        try:
            data=graph.run(query3)
        except:
            print("Error on creation relation")

        #Create Relation between Offer and Application
        query3="MATCH (n: Artifact:Offer{Type: 'Offer', offerID: '"+offer_id+"'}),(m: Artifact:Application{Type: 'Application', applicationID: '"+application_id+"'})" \
                "MERGE (n)-[:Offered]->(m)"
        try:
            data=graph.run(query3)
        except:
            print("Error on creation relation")
        if activity_name=='O_Cancelled':
            #Create canceledOffer relation
            query3="MATCH (n: Artifact:Offer{Type: 'Offer', offerID: '"+offer_id+"'}),(m: Artifact:Application{Type: 'Application', applicationID: '"+application_id+"'})" \
                "MERGE (n)-[:CanceledOffer]->(m)"
            try:
                data=graph.run(query3)
            except:
                print("Error on creation relation")

    elif event_origin=='Workflow':
        #Worflow Artifact
        workflow_id=sheet.cell_value(i,15)
        #print("workflof id: "+workflow_id)
        if workflow_id not in workflow_list:
            workflow_list.append(workflow_id)
            #Create Workflow node
            query2="CREATE (m: Artifact:Workflow {Type: 'Workflow', workflowID: '"+workflow_id+"'})"
            try:
                data=graph.run(query2)
            except:
                print("workflow not created "+workflow_id)
            print("Workflow Created: "+workflow_id)

        #Create Relation between Workflow and Activity
        query3="MATCH (n: Artifact:Workflow{Type: 'Workflow', workflowID: '"+workflow_id+"'}),(m: Activity { ID:'"+activity_id+"'})" \
                "MERGE (m)-[:AffectArtifact]->(n)"
        try:
            data=graph.run(query3)
        except:
            print("Error on creation relation")

        #Create relation between Workflow and Application
        query3="MATCH (n: Artifact:Workflow{Type: 'Workflow', workflowID: '"+workflow_id+"'}),(m: Artifact:Application{Type: 'Application', applicationID: '"+application_id+"'})" \
                "MERGE (n)-[:WorkOf]->(m)"
        try:
            data=graph.run(query3)
        except:
            print("Error on creation relation")

        offerID=sheet.cell_value(i,11)
        if not offerID=='':
            #Create Relation between Offer and Activity
            query3="MATCH (n: Artifact:Offer{Type: 'Offer', offerID: '"+offerID+"'}),(m: Activity { ID:'"+activity_id+"'})" \
                "MERGE (m)-[:AffectArtifact]->(n)"
            try:
                data=graph.run(query3)
            except:
                print("Error on creation relation")

    i=i+1


#Create ApplicationFollowedBy relation
for appID in application_list:
    query="MATCH (a: Activity)-[:AffectArtifact]->(s: Artifact {Type:'Application', applicationID: '"+appID+"'}) " \
           "RETURN a.ID order by a.ID desc"
    try:
        data=graph.run(query).to_table()
    except:
        print("Error when retrieving data")
    last_activity_id=0
    for record in data:
        activity_id=record[0]
        if not last_activity_id==0:
                query = "MATCH (n: Activity{ ID:'" + last_activity_id + "'}),(m: Activity { ID:'" + str(activity_id) + "'})" \
                        "MERGE (n)<-[:ApplicationFollowedBy {artifactID: '"+appID+"'}]-(m)"
                try:
                    data = graph.run(query)
                except:
                    print("Error when creating ApplicationFollowedBy relation")
        last_activity_id = activity_id

#Create OfferFollowedBy relation
for offerID in offer_list:
    query="MATCH (a: Activity)-[:AffectArtifact]->(s: Artifact {Type:'Offer', offerID: '"+offerID+"'}) " \
           "RETURN a.ID order by a.ID desc"
    try:
        data=graph.run(query).to_table()
    except:
        print("Error when retrieving data")
    last_activity_id=0
    for record in data:
        activity_id=record[0]
        if not last_activity_id==0:
                query = "MATCH (n: Activity{ ID:'" + last_activity_id + "'}),(m: Activity { ID:'" + str(activity_id) + "'})" \
                        "MERGE (n)<-[:OfferFollowedBy {artifactID: '"+offerID+"'}]-(m)"
                try:
                    data = graph.run(query)
                except:
                    print("Error when creating OfferFollowedBy relation")
        last_activity_id = activity_id

#Create WorkflowFollowedBy relation
for workID in workflow_list:
    query="MATCH (a: Activity)-[:AffectArtifact]->(s: Artifact {Type:'Workflow', workflowID: '"+workID+"'}) " \
           "RETURN a.ID order by a.ID desc"
    try:
        data=graph.run(query).to_table()
    except:
        print("Error when retrieving data")
    last_activity_id=0
    for record in data:
        activity_id=record[0]
        if not last_activity_id==0:
                query = "MATCH (n: Activity{ ID:'" + last_activity_id + "'}),(m: Activity { ID:'" + str(activity_id) + "'})" \
                        "MERGE (n)<-[:WorkflowFollowedBy {artifactID: '"+workID+"'}]-(m)"
                try:
                    data = graph.run(query)
                except:
                    print("Error when creating WorkflowFollowedBy relation")
        last_activity_id = activity_id

print(i)
print("--- %s seconds ---" % (time.time() - start_time))
