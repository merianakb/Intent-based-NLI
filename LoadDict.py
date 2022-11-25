import json
dictinary = json.load(open("C:/Users/user/Desktop/Courses/Master2/Stage/MyPapers/chatbot/Marwa Files/dic_actType_BD2m__forney.txt"))
for item in dictinary:
    print(item)
    print(dictinary[item])
    print()

print(len(dictinary))


