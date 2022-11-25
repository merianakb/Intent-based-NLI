from math import sqrt

import xlrd

# Give the location of the file
loc = ("C:/Users/HP/Desktop/Courses/PhD/MyPapers/ICPM/Evaluation/BPI_Evaluation result.xlsx")


# To open Workbook
wb = xlrd.open_workbook(loc)
sheet = wb.sheet_by_index(0)

def getMin(array):
    min=100
    i=0
    while i<len(array):
        if array[i]<min:
            min=array[i]
        i=i+1
    return min

def getMax(array):
    max = 0
    i = 0
    while i < len(array):
        if array[i] > max:
            max = array[i]
        i = i + 1
    return max

def getSD(array, avg):
    i=0
    sum=0
    while i<len(array):
        sum=sum+(array[i]-avg)**2
        i=i+1
    return sqrt(sum/100)


i=2
time_NLP=[]
time_query=[]
time_execution=[]
time_NLP_sum=0
time_query_sum=0
time_execution_sum=0

while i<102:
    time_NLP.append(float(sheet.cell_value(i,8)))
    time_NLP_sum=time_NLP_sum+float(sheet.cell_value(i,8))

    time_query.append(float(sheet.cell_value(i,9)))
    time_query_sum = time_query_sum + float(sheet.cell_value(i, 9))

    time_execution.append(sheet.cell_value(i,10))
    time_execution_sum = time_execution_sum + float(sheet.cell_value(i, 10))
    i=i+1


print ('NLP')
print(time_NLP_sum/100)
print(getMin(time_NLP))
print(getMax(time_NLP))
print(getSD(time_NLP,time_NLP_sum/100))

print ('Query')
print(time_query_sum/100)
print(getMin(time_query))
print(getMax(time_query))
print(getSD(time_query,time_query_sum/100))

print ('Execution')
print(time_execution_sum/100)
print(getMin(time_execution))
print(getMax(time_execution))
print(getSD(time_execution,time_execution_sum/100))