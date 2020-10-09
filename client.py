
from threading import Thread
import socket
sep1='!!!!!separator!!!!!'
sep2='*****seperator*****'

def receive():
    global client
    global details, sep1, sep2,result,groupfull,members,memberslist
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
            elif m[0:7]=="details":
                x=m.split(sep1)
                y=[]
                for i in range(1,len(x)-1):
                    y.append(x[i].split(sep2))
                details=y                                       #details=[[groupname,limit,groupcode]]
                print(y)
            elif m[0:8]=="$$auth$$":
                print(m)
                if m[8]=="t":
                    result=True
                    groupfull=False
                elif m[8]=="f":
                    result=False
                    groupfull=False
                elif m[8]=="g":
                    result=False
                    groupfull=True
            elif m[0:12]=="$$$length$$$":
                x=m.split(sep1)
                for i in range(1,len(x)-1):
                    y=x[i].split(sep2)
                    members[y[0]]=int(y[1])
            elif m[0:11]=="$$memlist$$":
                x=m.split(sep2)
                n=len(x)-1
                memberslist=x[1:n]


        except OSError:
           print("Connection got disconnected")
           break
def return_details():
    global details
    print('from client script:  ')
    print(details)
    return details

def return_authenticate():
    global result
    print('from client side:' + str(result))
    return result

def return_groupfull():
    global groupfull
    print('from client side:' + str(groupfull))
    return groupfull

def return_members():
    global members
    return members

def return_memeberslist():
    global memberslist
    return memberslist

def sendName(username):
    global client
    print("sendname")
    client.send(username.encode('ASCII'))

def sendGroups():
    global client
    client.send("groups".encode('ASCII'))

def sendMembers():
    global client
    client.send("members".encode('ASCII'))

def sendMembersList():
    global client
    client.sendall("membersList".encode("ASCII"))

def sendCreate(s):
    global client
    client.send("create".encode('ASCII'))
    client.send(s.encode("ASCII"))
    print('sent-create-request')

def sendJoin(s):
    global client
    client.send("join".encode('ASCII'))
    client.send(s.encode('ASCII'))
    print('sent-join-request')

def sendLogout():
    global client
    client.send("QUIT".encode('ASCII'))
    print('sendlogout')

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
result=None
groupfull=None
members={}
memberslist=[]
#Host=input("Enter the host name: ")
#Port=int(input("Enter the port number: "))
#Host="34.227.91.249"
def client_initialize():
    global client
    client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    Host="127.0.0.1"
    Port=8000
    client.connect((Host,Port))
    rthread=Thread(target=receive)
    rthread.start()


    

