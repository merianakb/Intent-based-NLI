import xlrd

from py2neo import Graph
from datetime import datetime

activity_list=[]
actor_list=[]

def floatHourToTime(fh):
    h, r = divmod(fh, 1)
    m, r = divmod(r*60, 1)
    return (
        int(h),
        int(m),
        int(r*60),
    )


# Give the location of the file
loc = ("C:/Users/user/Desktop/Courses/Master2/Stage/MyPapers/chatbot/testing_data_v1.xlsx")

# To open Workbook
wb = xlrd.open_workbook(loc)
sheet = wb.sheet_by_index(0)

i=2
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

    if activity_name not in activity_list:
        activity_list.append(activity_name)
    if actor_from not in actor_list:
        actor_list.append(actor_from)
    if actor_executor not in actor_list:
        actor_list.append(actor_executor)
    if actor_requestor not in actor_list:
        actor_list.append(actor_requestor)
    if actor_requested not in actor_list:
        actor_list.append(actor_requested)
    for actor in actor_cc:
        actor=actor.split()
        if actor not in actor_list:
            actor_list.append(actor)
    for actor in actor_to:
        actor=actor.split()
        if actor not in actor_to:
            actor_list.append(actor)
    i=i+1
