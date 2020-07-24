
from threading import Thread
import socket
import tkinter



def receive(client):
    i=1
    while 1:
        m=client.recv(1024)
        try:
            m=m.decode("ASCII")
        except OSError:
           print("Connection got disconnected")
           break


def send(event=None):
    message= message.get()
    message.set("")
    message=message.encode("ASCII")
    client.send(message)
    if message=="QUIT":
        client.close()
        window.quit()                #closes even the gui window

def close(event=None):
    m="QUIT"
    message.set(m)             #settting the variable of text-input to QUIT
    send()                     #this is like clicking send button automatically
    

#############################GUI

window=tkinter.Tk()
window.title("chat-app")

#frame+scrollbar+listboxes
frame=tkinter.Frame(window)
scrollbar=tkinter.Scrollbar(frame)
list=tkinter.Listbox(frame,height=15,width=50,yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
list.pack()
frame.pack()

#str variable+sendbtn+inputfield

message=tkinter.StringVar() #this variable is only used for all the functions to be done on the input field.. In simple terms for accessing the input field u need this var!!
message.set("Type your messages here...")
inputfield=tkinter.Entry(window, textvariable=message)
inputfield.bind("<Return>",send)   #ntg but attaching send function to input field
sendbtn=tkinter.Button(window,text="Send",command=send) #command=send binds it with the send function
sendbtn.pack()


#binding the window closing event to close function
window.protocol("WM_DELETE_WINDOW",close)













client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
Host=input("Enter the host name: ")
Port=int(input("Enter the port number: "))
client.connect((Host,Port))  
rthread=Thread(target=receive,args=(client,))
rthread.start()
tkinter.mainloop() # starts the gui window!

    

