#CreatedOn 15/9/2020
import tkinter
import json
from tkinter import *

from MainClass import chatbot_response


def send():
    msg = EntryBox.get("1.0",'end-1c').strip()
    EntryBox.delete("0.0",END)

    if msg != '':
        ChatLog.config(state=NORMAL)
        ChatLog.config(foreground="#442265", font=("Verdana", 12 ))
        ChatLog.insert(END, "You: " + msg + '\n\n')


        print(msg)
        res = chatbot_response(msg)
        print(res)
        output=''
        if(res=='Error' or res==' '):
            output='Error, please repeat the question with another syntax'
        else:
            for record in res:
                output=output+str(record)+'\n'

        #ChatLog.config(foreground="#000000", font=("Verdana", 12 ))
        ChatLog.tag_config('bg_yellow', background='yellow')
        ChatLog.insert(END, "Bot: "+ output,'bg_yellow')
        ChatLog.insert(END,'\n\n')


        ChatLog.config(state=DISABLED)
        ChatLog.yview(END)
        msg=''


base = Tk()
base.title("Hello")
base.geometry("500x600")
base.resizable(width=FALSE, height=FALSE)

#Create Chat window
ChatLog = Text(base, bd=0, bg="white", height="8", width="50", font="Arial",)

ChatLog.config(state=DISABLED)

#Bind scrollbar to Chat window
scrollbar = Scrollbar(base, command=ChatLog.yview, cursor="arrow")
ChatLog['yscrollcommand'] = scrollbar.set

#Create Button to send message
SendButton = Button(base, font=("Verdana",12,'bold'), text="Send", width="12", height=5,
                    bd=0, bg="#32de97", activebackground="#3c9d9b",fg='#ffffff',
                    command= send )

#Create the box to enter message
EntryBox = Text(base, bd=0, bg="white",width="29", height="5", font="Arial")
#EntryBox.bind("<Return>", send)


#Place all components on the screen
scrollbar.place(x=480,y=6, height=406)
ChatLog.place(x=6,y=6, height=400, width=470)
EntryBox.place(x=128, y=420, height=90, width=350)
SendButton.place(x=6, y=420, height=90)

base.mainloop()
