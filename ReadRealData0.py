import xlrd

from py2neo import Graph
from datetime import datetime

activity_list=[]
actor_list=[]
subject_list=[]
position_list=[]
application_list=[]
candidate_list=[]
interview_list=[]

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
loc = ("C:/Users/HP/Desktop/Courses/Stage/MyPapers/chatbot/testing_data_hiring.xlsx")

# To open Workbook
wb = xlrd.open_workbook(loc)
sheet = wb.sheet_by_index(0)

i=2
last_activity_id=0

while i<sheet.nrows:
    activity_name=sheet.cell_value(i,7)
    activity_nature=sheet.cell_value(i,17)
    activity_id=str(i)

    actor_from=sheet.cell_value(i,1)
    actor_cc=sheet.cell_value(i,2).split(";")
    actor_to=sheet.cell_value(i,3).split(";")
    actor_executor=sheet.cell_value(i,18)
    actor_requestor=sheet.cell_value(i,20)
    actor_requested=sheet.cell_value(i,21)

    print("activityname: "+activity_name+" /activitynature: "+activity_nature+" /from: "+actor_from+" /to:  "+actor_to[0])
    if activity_name not in activity_list:
        activity_list.append(activity_name)


    #create activity node
    query="CREATE (n: Activity {activityName: '"+activity_name+"',activityNature: '"+activity_nature+"' ,ID: '"+activity_id+"'})"
    try:
        data=graph.run(query)
    except:
        print("activity not created "+activity_name+"i")

    #create followedBy relation
    if not last_activity_id==0:
        query = "MATCH (n: Activity{ ID:'" + last_activity_id + "'}),(m: Activity { ID:'" + activity_id + "'})" \
                  "MERGE (n)-[:FollowedBy]->(m)"
        try:
            data = graph.run(query)
        except:
            print("Error on creation FollowedBy relation")
    last_activity_id=activity_id


    #create actor with hasSent relation
    query2="MERGE (m: Actor {actorEmail: '"+actor_from+"'})"
    try:
        data=graph.run(query2)
    except:
        print("actor not created "+actor_from)
    query3="MATCH (n: Actor{actorEmail: '"+actor_from+"'}),(m: Activity { ID:'"+activity_id+"'})" \
                "MERGE (n)-[:HasSent]->(m)"
    try:
        data=graph.run(query3)
    except:
        print("Error on creation relation")
    if actor_from not in actor_list:
        actor_list.append(actor_from)

    #create actor with hasReceived relation
    for actor in actor_to:
        actor=actor.strip()
        query2="MERGE (m: Actor {actorEmail: '"+actor+"'})"
        try:
            data=graph.run(query2)
        except:
            print("actor not created "+actor)
        query3="MATCH (n: Actor{actorEmail: '"+actor+"'}),(m: Activity { ID:'"+activity_id+"'})" \
                "MERGE (n)-[:HasReceived]->(m)"
        try:
            data=graph.run(query3)
        except:
            print("Error on creation relation")
        if actor not in actor_list:
            actor_list.append(actor)

     #create actor with hasObserved relation
    for actor in actor_cc:
        actor=actor.strip()
        query2="MERGE (m: Actor {actorEmail: '"+actor+"'})"
        try:
            data=graph.run(query2)
        except:
            print("actor not created "+actor)
        query3="MATCH (n: Actor{actorEmail: '"+actor+"'}),(m: Activity { ID:'"+activity_id+"'})" \
                "MERGE (n)-[:HasObserved]->(m)"
        try:
            data=graph.run(query3)
        except:
            print("Error on creation relation")
        if actor not in actor_list:
            actor_list.append(actor)

    #create actor with hasExecuted relation
    query2="MERGE (m: Actor {actorEmail: '"+actor_executor+"'})"
    try:
        data=graph.run(query2)
    except:
        print("actor not created "+actor_executor)
    query3="MATCH (n: Actor{actorEmail: '"+actor_executor+"'}),(m: Activity { ID:'"+activity_id+"'})" \
                "MERGE (n)-[:HasExecuted]->(m)"
    try:
        data=graph.run(query3)
    except:
        print("Error on creation relation")
    if actor_executor not in actor_list:
            actor_list.append(actor_executor)

    #create actor with hasRequested relation
    query2="MERGE (m: Actor {actorEmail: '"+actor_requestor+"'})"
    try:
        data=graph.run(query2)
    except:
        print("actor not created "+actor_requestor)
    query3="MATCH (n: Actor{actorEmail: '"+actor_requestor+"'}),(m: Activity { ID:'"+activity_id+"'})" \
                "MERGE (n)-[:HasRequested]->(m)"
    try:
        data=graph.run(query3)
    except:
        print("Error on creation relation")
    if actor_requestor not in actor_list:
            actor_list.append(actor_requestor)

    #create actor with hasReceivedRequest relation
    query2="MERGE (m: Actor {actorEmail: '"+actor_requested+"'})"
    try:
        data=graph.run(query2)
    except:
        print("actor not created "+actor_requested)
    query3="MATCH (n: Actor{actorEmail: '"+actor_requested+"'}),(m: Activity { ID:'"+activity_id+"'})" \
                "MERGE (n)-[:HasReceivedRequest]->(m)"
    try:
        data=graph.run(query3)
    except:
        print("Error on creation relation")
    if actor_requested not in actor_list:
            actor_list.append(actor_requested)

    #Subject artifact
    subject=sheet.cell_value(i,8)
    if not len(subject)==0:
        query2="MERGE (m: Artifact {Type:'Subject', subjectTitle: '"+subject+"'})"
        try:
            data=graph.run(query2)
        except:
            print("subject not created "+subject)

        if not subject in subject_list:
            subject_list.append(subject)

        query3="MATCH (m: Artifact {Type:'Subject', subjectTitle: '"+subject+"'}),(n: Activity { ID:'"+activity_id+"'})" \
                "MERGE (n)-[:AffectArtifact]->(m)"
        try:
            data=graph.run(query3)
        except:
            print("Error on creation relation")


    #Position artifact
    position=sheet.cell_value(i,10)
    if not len(position)==0:
        query2="MERGE (m: Artifact {Type:'Position', positionTitle: '"+position+"'})"
        try:
            data=graph.run(query2)
        except:
            print("position not created "+position)

        if not position in position_list:
            position_list.append(position)

        query3="MATCH (m: Artifact {Type:'Position', positionTitle: '"+position+"'}),(n: Activity { ID:'"+activity_id+"'})" \
                "MERGE (n)-[:AffectArtifact]->(m)"
        try:
            data=graph.run(query3)
        except:
            print("Error on creation relation")


    #Interview artifact
    date=sheet.cell_value(i,11)
    time=str(sheet.cell_value(i,12))
    location=sheet.cell_value(i,13)
    if not len(str(date))==0:
        dt = datetime.fromordinal(datetime(1900, 1, 1).toordinal() + int(date) - 2)
        hour, minute, second = floatHourToTime(date % 1)
        dt = dt.replace(hour=hour, minute=minute, second=second)
        dateString=dt.strftime("%d-%b-%Y")
        query2="MERGE (m: Artifact {Type:'Interview', interviewDate: '"+dateString+"', interviewTime: '"+time+"', interviewLocation: '"+location+"'})"
        try:
            data=graph.run(query2)
        except:
            print("interview not created ")

        interview=dateString+";"+time+";"+location
        if not interview in interview_list:
            interview_list.append(interview)

        query3="MATCH (m: Artifact {Type:'Interview', interviewDate: '"+dateString+"', interviewTime: '"+time+"', interviewLocation: '"+location+"'}),(n: Activity { ID:'"+activity_id+"'})" \
                "MERGE (n)-[:AffectArtifact]->(m)"
        try:
            data=graph.run(query3)
        except:
            print("Error on creation relation")

    #Application artifact
    number=sheet.cell_value(i,14).split(",")
    status=sheet.cell_value(i,15)
    if not len(number)==0:
        for num in number:
            num=num.strip()
            if num=='':
                continue
            query2="MERGE (m: Artifact {Type:'Application', applicationNumber: '"+num+"'})"
            try:
                data=graph.run(query2)
            except:
                print("application not created "+num)

            if not num in application_list:
                application_list.append(num)

            query3="MATCH (m: Artifact {Type:'Application', applicationNumber: '"+num+"'}),(n: Activity { ID:'"+activity_id+"'})" \
                "MERGE (n)-[:AffectArtifact]->(m)"
            try:
                data=graph.run(query3)
            except:
                print("Error on creation relation")

            #HasApplication relation between application and candidate nodes
            cand=num.replace('app','Candidate')
            query3 = "MATCH (m: Artifact {Type:'Candidate', candidateName: '" + cand + "'}),(n: Artifact {Type:'Application', applicationNumber: '"+num+"'})" \
                        "MERGE (m)-[:HasApplication]->(n)"
            try:
                data = graph.run(query3)
            except:
                print("Error on creation relation")


            #ForPosition relation between application and position nodes
            if not len(position)==0:
                query3 = "MATCH (m: Artifact {Type:'Application', applicationNumber: '" + num + "'}),(n: Artifact {Type:'Position', positionTitle:'" + position + "'})" \
                           "MERGE (m)-[:ForPosition]->(n)"
                try:
                    data = graph.run(query3)
                except:
                    print("Error on creation relation")


            if not len(status)==0: #accepted or rejected
                for cand in candidate:
                    cand=cand.strip()
                    if cand=='':
                        continue
                    query3="MATCH (m: Artifact {Type:'Candidate', candidateName: '"+cand+"'}),(n: Artifact {Type:'Position', positionTitle:'"+position+"'})" \
                            "MERGE (m)-[:"+status+"]->(n)"
                    try:
                        data=graph.run(query3)
                    except:
                        print("Error on creation relation")
                    if not len(position)==0:
                        query3="MATCH (m: Artifact {Type:'Application', applicationNumber: '"+num+"'}),(n: Artifact {Type:'Position', positionTitle:'"+position+"'})" \
                            "MERGE (m)-[:"+status+"]->(n)"
                        try:
                            data=graph.run(query3)
                        except:
                            print("Error on creation relation")



    #Candidate artifact
    candidate=sheet.cell_value(i,16).split(",")

    if not len(candidate)==0:
        for cand in candidate:
            cand=cand.strip()
            if cand=='':
                continue
            query2="MERGE (m: Artifact {Type:'Candidate', candidateName: '"+cand+"'})"
            try:
                data=graph.run(query2)
            except:
                print("candidate not created "+cand)

            if not cand in candidate_list:
                candidate_list.append(cand)

            query3="MATCH (m: Artifact {Type:'Candidate', candidateName: '"+cand+"'}),(n: Activity { ID:'"+activity_id+"'})" \
                    "MERGE (n)-[:AffectArtifact]->(m)"
            try:
                data=graph.run(query3)
            except:
                print("Error on creation relation")

    i=i+1


#Create SubjectFollowedBy relation
for subject in subject_list:
    query="MATCH (a: Activity)-[:AffectArtifact]->(s: Artifact {Type:'Subject', subjectTitle: '"+subject+"'}) " \
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
                        "MERGE (n)<-[:SubjectFollowedBy {artifactID: '"+subject+"'}]-(m)"
                try:
                    data = graph.run(query)
                except:
                    print("Error when creating SubjectFollowedBy relation")
        last_activity_id = activity_id

#Create PositionFollowedBy relation
for position in position_list:
    query="MATCH (a: Activity)-[:AffectArtifact]->(p: Artifact {Type:'Position', positionTitle: '"+position+"'}) " \
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
                        "MERGE (n)<-[:PositionFollowedBy {artifactID: '"+position+"'}]-(m)"
                try:
                    data = graph.run(query)
                except:
                    print("Error when creating PositionFollowedBy relation")
        last_activity_id = activity_id

#Create ApplicationFollowedBy relation
for application in application_list:
    query="MATCH (a: Activity)-[:AffectArtifact]->(p: Artifact {Type:'Application', applicationNumber: '"+application+"'}) " \
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
                        "MERGE (n)<-[:ApplicationFollowedBy {artifactID: '"+application+"'}]-(m)"
                try:
                    data = graph.run(query)
                except:
                    print("Error when creating ApplicationFollowedBy relation")
        last_activity_id = activity_id

#Create CandidateFollowedBy relation
for candidate in candidate_list:
    query="MATCH (a: Activity)-[:AffectArtifact]->(p: Artifact {Type:'Candidate', candidateName: '"+candidate+"'}) " \
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
                        "MERGE (n)<-[:CandidateFollowedBy {artifactID: '"+candidate+"'}]-(m)"
                try:
                    data = graph.run(query)
                except:
                    print("Error when creating CandidateFollowedBy relation")
        last_activity_id = activity_id

#Create InterviewFollowedBy relation
for interview in interview_list:
    date,time,location=interview.split(";")
    query="MATCH (a: Activity)-[:AffectArtifact]->(p: Artifact {Type:'Interview', interviewDate: '"+date+"', interviewTime: '"+time+"', interviewLocation: '"+location+"'}) " \
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
                        "MERGE (n)<-[:InterviewFollowedBy {artifactID: '"+interview+"'}]-(m)"
                try:
                    data = graph.run(query)
                except:
                    print("Error when creating InterviewFollowedBy relation")
        last_activity_id = activity_id






