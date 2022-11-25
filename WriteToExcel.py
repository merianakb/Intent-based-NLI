import xlwt
from xlwt import Workbook

from LoadDict3 import getArtifactOfBD
from ReadFromExcel2 import activities_list, activity_actKey


def arrayToList(array):
    s=""
    for item in array:
        data=item[0]
        value=item[1]
        s+=data+": "+value
        s+=" ;  "

    return s

# Workbook is created
wb = Workbook()

# add_sheet is used to create sheet.
sheet1 = wb.add_sheet('Sheet 1')

visited=[]
dictArray=[]
i=0
counter=0
size=len(activities_list)
while i<size:
    item=activities_list[i]
    activity=item['activityInstance']
    activityKey=activity_actKey[activity.split("__")[0].strip()]
    if not activityKey in visited:
        visited.append(activityKey)
        dictActivity={}
        dictActivity['activityInstance']=activity
        dictActivity['businessData']=item['businessData']
        dictActivity['businessDataValue']=item['businessDataValue']
        dictArray.append(dictActivity)
        j=i+1
        while j<size:
            item2=activities_list[j]
            activity2=item2['activityInstance']
            activityKey2=activity_actKey[activity2.split("__")[0].strip()]
            if activityKey2==activityKey:
                dictActivity={}
                dictActivity['activityInstance']=activity2
                dictActivity['businessData']=item2['businessData']
                dictActivity['businessDataValue']=item2['businessDataValue']
                dictArray.append(dictActivity)

            j=j+1

    i=i+1

for item in dictArray:
    print(item)
print(len(dictArray))

sheet1.write(0,0,'activityInstance')
sheet1.write(0,1,'businessData')
sheet1.write(0,2,'businessDataValue')
sheet1.write(0,3,'artifact')

i=0
j=1
while i<len(dictArray):
    item=dictArray[i]
    sheet1.write(j,0,item['activityInstance'])
    sheet1.write(j,1,item['businessData'])
    sheet1.write(j,2,arrayToList(item['businessDataValue']))

    artifact=getArtifactOfBD(item['businessData'].strip())
    sheet1.write(j,3,artifact)
    i=i+1
    j=j+1

wb.save('C:/Users/user/Desktop/Courses/Master2/Stage/MyPapers/chatbot/Marwa Files/activityBDOutput.xls')

