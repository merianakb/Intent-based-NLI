import json
dictinary = json.load(open("C:/Users/user/Desktop/Courses/Master2/Stage/MyPapers/chatbot/Marwa Files/dic_patterns_org_ids.txt"))
for item in dictinary:
    print(item)
    print(dictinary[item])
    print()

print(len(dictinary))

item=dictinary['buy_purchase hour0end numeric numeric0mwTvnnn']['<893233.1075852367894.JavaMail.evans@thyme>'][0]
if(len(item)!=0):
    i=0
    while i<len(item):
        print(item[i][0]+" "+item[i][1])
        i=i+1
