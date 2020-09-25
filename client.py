
from threading import Thread
import socket
import tkinter



def receive():
    i=1
    while 1:
        try:
            m=client.recv(1024)
            m=m.decode("ASCII")
            print(m)
            
            listm.insert(tkinter.END,m)
            if(m[0:3]=="Bye"):
                client.close()
                window.destroy()                #closes even the gui window
                
        except OSError:
           print("Connection got disconnected")
           break

def sendName():
    client.send()
    
def sendGroups(c):
    m= message.get()
    message.set("")
    m=m.encode("ASCII")
    client.send(m)
    client.send("groups".encode('ASCII')) 

def sendCreate(s):
    client.send("create".encode('ASCII'))
    client.send(s.encode("ASCII"))
    
        

def close(event=None):
    m="QUIT".encode("ASCII")                  #settting the variable of text-input to QUIT
    client_socket.send(m)                     #this is like clicking send button automatically
    
def close2():
    client_socket.close()

#############################GUI

window=tkinter.Tk()
window.title("chat-app")

#frame+scrollbar+listboxes
frame=tkinter.Frame(window)
message=tkinter.StringVar() #this variable is only used for all the functions to be done on the input field.. In simple terms for accessing the input field u need this var!!
message.set("Type your messages here...")
scrollbar=tkinter.Scrollbar(frame)
listm=tkinter.Listbox(frame,height=20,width=100,yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
listm.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
listm.pack()
frame.pack()
#str variable+sendbtn+inputfield
inputfield=tkinter.Entry(window, textvariable=message)
inputfield.bind("<Return>",send)   #ntg but attaching send function to input field
inputfield.pack()
sendbtn=tkinter.Button(window,text="Send",command=send) #command=send binds it with the send function
sendbtn.pack()


#binding the window closing event to close function
window.protocol("WM_DELETE_WINDOW",close)



client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#Host=input("Enter the host name: ")
#Port=int(input("Enter the port number: "))
#Host="34.227.91.249"
Host="127.0.0.1"
Port=8080
client.connect((Host,Port))  
rthread=Thread(target=receive)
rthread.start()
tkinter.mainloop() # starts the gui window!

    

