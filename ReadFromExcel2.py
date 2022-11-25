import json

import xlrd

###mapping between activity and activity key
activity_actKey={}

###list with information about all activities
activities_list=[]


def removeLast_(activityKey):
    parts=activityKey.split("_")
    actKey=""
    i=0
    while i<len(parts)-1:
        actKey=actKey+parts[i]
        if( i<len(parts)-2):
            actKey=actKey+"_"
        i=i+1
    actKey=actKey+parts[i]
    return actKey


##########################fill activity_actkey dictionary###################################################
loc = ("C:/Users/user/Desktop/Courses/Master2/Stage/MyPapers/chatbot/Marwa Files/resultm__forney.xlsx")

# To open Workbook
wb = xlrd.open_workbook(loc)
sheet = wb.sheet_by_index(0)
i=1
while i<sheet.nrows:
    activityLabel=sheet.cell_value(i,1)
    activityKey=sheet.cell_value(i,4)
    activity_actKey[activityLabel]=removeLast_(activityKey)
    i=i+1




###########################dictionary mapping between activity key and BD######################################
BD_dictionary = json.load(open("C:/Users/user/Desktop/Courses/Master2/Stage/MyPapers/chatbot/Marwa Files/dic_actType_BD2m__forney.txt"))

###########################dictionary mapping between each BD and value in email ID############################
BDValue_dictionary = json.load(open("C:/Users/user/Desktop/Courses/Master2/Stage/MyPapers/chatbot/Marwa Files/dic_patterns_org_ids.txt"))



############################fill the information about each activity############################################
loc = ("C:/Users/user/Desktop/Courses/Master2/Stage/MyPapers/chatbot/Marwa Files/activityInstancesm__forney.xlsx")
wb = xlrd.open_workbook(loc)
sheet = wb.sheet_by_index(0)
i=1
instance=0
while i<sheet.nrows:
    ###add information about each activity
    activity_dict={}
    activityInstance=sheet.cell_value(i,4)
    activityKey=activity_actKey[activityInstance]
    support=sheet.cell_value(i,5)
    emailID=sheet.cell_value(i,2)
    activity_dict['activityInstance']=str(activityInstance)+"__"+str(instance)
    activity_dict['activityKey']=activityKey
    activity_dict['support']=support
    activity_dict['businessData']=''
    activity_dict['businessDataValue']=''

    inserted=0
    if(activityKey in BD_dictionary):
        BD_of_activity=BD_dictionary[activityKey]['bd']
        for businessData in BD_of_activity:
            if(businessData in BDValue_dictionary and emailID in BDValue_dictionary[businessData]):
                if inserted==1:
                    activity_dict={}
                    activity_dict['activityInstance']=str(activityInstance)+"__"+str(instance)
                    activity_dict['activityKey']=activityKey
                    activity_dict['support']=support
                businessData_values=BDValue_dictionary[businessData][emailID][0]
                activity_dict['businessDataValue']=businessData_values
                activity_dict['businessData']=businessData
                activities_list.append(activity_dict)
                inserted=1

    if inserted==0:
        activities_list.append(activity_dict)
    i=i+1
    instance=instance+1




