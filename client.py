
from threading import Thread
import copy
import socket
import pickle
sep1='!!!!!separator!!!!!'
sep2='*****seperator*****'

HEADER_SIZE=10

def receive():
    global client
    global details, sep1, sep2,result,groupfull,members,memberslist,clientmessageList,name
    i=1
    #print('Function Started!!!!')
    while 1:
        try:
            length=client.recv(HEADER_SIZE).decode('UTF-8')
            #print("legnth: "+str(length))
            m=client.recv(int(length)).decode('UTF-8')
            #print("message:"+str(m))
            if m[0:3]=="Bye":
                client.close()
                print("Connection got disconnected.............")
                break
            elif m[0:7]=="details":
                print("details")
                message=client.recv(int(m[7:]))
                details=pickle.loads(message)        #details={'groupname':'[limit,code,length]'}
            elif m[0:4]=="auth":
                length=int(m[4:])
                obj=pickle.loads(client.recv(length))
                result=obj["result"]
                groupfull=obj["groupfull"]
                if result==True and groupfull==True:
                      clientmessageList.append({
                       'colour':"#00a343",
                       'name':"ChatBot",
                       'message':"Welcome {} to the Crypto Chamber! Start sharing your secrets!!".format(name)
                     })
                #print(m)
                # if m[8]=="t":
                #     print("auth successfull")
                #     result=True
                #     groupfull=False
                # elif m[8]=="f":
                #     print("auth failed password wrong")
                #     result=False
                #     groupfull=False
                # elif m[8]=="g":
                #     print("auth failed group full")
                #     result=False
                #     groupfull=True
            # elif m[0:12]=="$$$length$$$":
            #     x=m.split(sep1)
            #     for i in range(1,len(x)-1):
            #       #  print('print x from client'+str(x))
            #         y=x[i].split(sep2)
            #         members[y[0]]=int(y[1])
            elif m[0:11]=="membersList":
                listobj=pickle.loads(client.recv(int(m[11:])))
                memberslist=listobj["0"]
            elif m[0:9]=="memberadd":
                addobj=pickle.loads(client.recv(int(m[9:])))
                memberslist.append(addobj['name'])
                # clientmessageList.append({
                #      'colour':"#00a343",
                #      'name':"ChatBot",
                #      'message': addobj['message']
                # })
            elif m[0:11]=="oldmessages":
                oldmessages=pickle.load(client.recv(int(m[11:])))
                clientmessageList=copy.deepcopy(oldmessages["0"])
            elif m[0:11]=="$$message$$":
                obj={}
                x=m.split(sep2)
                obj["colour"]=x[1]               #{"colour":value , "name": value, "message": value }
                obj["name"]=x[2]
                obj["message"]=x[3]
                print(obj)
                clientmessageList.append(obj)

        except OSError:
           print("Connection got disconnected")
           break


def return_details():
    global details
    print("details: "+str(details))
    return details

def return_authenticate():
    global result
   # print('from client side:' + str(result))
    return result

def return_groupfull():
    global groupfull
   # print('from client side:' + str(groupfull))
    return groupfull

def return_members():
    global members,details
    for x,y in details.items():
        members[x]=y[2]
    return members

def return_memeberslist():
    global memberslist
    return memberslist

def return_message():
    global clientmessageList,sentList
    if len(sentList)==0:
        sentList=copy.deepcopy(clientmessageList)
        print('a'+str(sentList))
        return sentList
    elif len(sentList)==len(clientmessageList):
        return []
    else:
        newMessages=clientmessageList[len(sentList):]
        for i in newMessages:
            sentList.append(i)
        print('c'+str(newMessages))
        return newMessages



def sendName(username):
    global client,name
    name=username
    name=username.encode('UTF-8')
    header=f"{len(name):<{HEADER_SIZE}}".encode("UTF-8")
    client.send(header+name)

def sendGroups():
    global client
    m="groups".encode('UTF-8')
    header=f"{len(m):<{HEADER_SIZE}}".encode("UTF-8")
    client.send(header+m)

def sendMembers():
    global client
    m="members".encode('UTF-8')
    header=f"{len(m):<{HEADER_SIZE}}".encode("UTF-8")
    client.send(header+m)

# def sendMembersList():
#     global client
#     client.sendall("membersList".encode("ASCII"))

def sendCreate(s):
    global client,memberslist,name
    m="create".encode('UTF-8')
    header=f"{len(m):<{HEADER_SIZE}}".encode("UTF-8")
    client.sendall(header+m)
    m=s.encode('UTF-8')
    header=f"{len(m):<{HEADER_SIZE}}".encode("UTF-8")
    client.sendall(header+m)
    print('sent-create-request')
    memberslist.append(name)
    clientmessageList.append({
        'colour':"#00a343",
        'name':"ChatBot",
        'message':"Welcome to your Crypto Chamber! Share Chamber Name and Code with your friends and have fun sharing secrets on crypto chamber!!"
    })

def sendJoin(s):
    global client
    client.send("join".encode('ASCII'))
    client.send(s.encode('ASCII'))
    print('sent-join-request')
    m="join".encode('UTF-8')
    header=f"{len(m):<{HEADER_SIZE}}".encode("UTF-8")
    client.sendall(header+m)
    m=s.encode('UTF-8')
    header=f"{len(m):<{HEADER_SIZE}}".encode("UTF-8")
    client.sendall(header+m)

def sendMessage(message,colour):
    global client
    m="message-"+colour+message
    client.sendall(m.encode("ascii"))

def sendLogout():
    global client,sentList,clientmessageList,sentList
    clientmessageList.clear()
    sentList.clear()
    m="QUIT".encode('UTF-8')
    header=f"{len(m):<{HEADER_SIZE}}".encode("UTF-8")
    client.sendall(header+m)
    print('sendlogout')


def close():
    global client
   # print('close')
    m="QUIT".encode("ASCII")                  #settting the variable of text-input to QUIT
    client.send(m)                     #this is like clicking send button automatically
    
def close2():
    global client
    client.close()



client=None
details={}
result=None
groupfull=None
members={}
memberslist=[]
clientmessageList=[]
sentList=[]
name=""
groupname=None

#Host=input("Enter the host name: ")
#Port=int(input("Enter the port number: "))
#Host="34.227.91.249"
def client_initialize():
    global client
    client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    Host="127.0.0.1"
    #Host="52.204.124.224"
    Port=8000
    client.connect((Host,Port))
    rthread=Thread(target=receive)
    rthread.start()


    

