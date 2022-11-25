import json
dictinary = json.load(open("C:/Users/user/Desktop/Courses/Master2/Stage/MyPapers/chatbot/Marwa Files/map.txt"))
'''''
for item in dictinary:
    print(item)
    print(dictinary[item])
    print()

print(len(dictinary))
'''
s1="hour0end numericTnn"
s2="book deal_tradeTnn"
s3="deal_trade locnameTnn"



def getArtifactOfBD(businessD):
    ###Eliminate Tnn from the end
    i=0
    businessData=''
    while i<len(businessD)-3:
        businessData+=businessD[i]
        i=i+1

    for item in dictinary:
        if businessData in dictinary[item]:
            print("item: "+item)
            return str(item)

