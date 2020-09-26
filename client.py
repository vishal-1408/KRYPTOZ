
from threading import Thread
import socket
sep1='!!!!!separator!!!!!'
sep2='*****seperator*****'
def receive():
    global client
    global details, sep1, sep2
    i=1
    print('Function Started!!!!')
    while 1:
        try:
            m=client.recv(1024)
            m=m.decode("ASCII")
            if m[0:3]=="Bye":
                client.close()
                print("Connection got disconnected.............")
                break
            if m[0:7]=="details":
                x=m.split(sep1)
                y=[]
                for i in range(1,len(x)-1):
                    y.append(x[i].split(sep2))
                details=y
                
                    
        except OSError:
           print("Connection got disconnected")
           break
def return_details():
    global details
    return details
def sendName(username):
    global client
    print("sendname")
    client.send(username.encode('ASCII'))
    
def sendGroups():
    global client
    client.sendall("groups".encode('ASCII')) 

def sendCreate(s):
    global client
    client.send("create".encode('ASCII'))
    client.send(s.encode("ASCII"))
    print('sent')
    
        



def close():
    global client
    print('close')
    m="QUIT".encode("ASCII")                  #settting the variable of text-input to QUIT
    client.send(m)                     #this is like clicking send button automatically
    
def close2():
    global client
    client.close()

#############################GUI
'''
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
'''

client=None
details=[]
#Host=input("Enter the host name: ")
#Port=int(input("Enter the port number: "))
#Host="34.227.91.249"
def client_initialize():
    global client
    client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    Host="127.0.0.1"
    Port=8080
    client.connect((Host,Port))
    rthread=Thread(target=receive)
    rthread.start()


    

