
from threading import Thread
import copy
import socket
import pickle
sep1='!!!!!separator!!!!!'
sep2='*****seperator*****'

HEADER_SIZE=10

def receive():
    global client
    global details, sep1, sep2,result,groupfull,members,memberslist,clientmessageList,name,groupdead
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
                #print("details")
                message=client.recv(int(m[7:]))
                details=pickle.loads(message)        #details={'groupname':'[limit,code,length]'}
            elif m[0:4]=="auth":
                length=int(m[4:])
                obj=pickle.loads(client.recv(length))
                print("object received:::::::::::::::::::::::::::::::::::::::::"+str(obj))
                result=obj["result"]
                groupfull=obj["groupfull"]
                # if result==True and groupfull==True:
                    #   clientmessageList.append({
                    #    'colour':"#223344",
                    #    'name':"ChatBot",
                    #    'message':"Welcome {} to the Crypto Chamber! Start sharing your secrets!!".format(name)
                    #  })
            elif m[0:11]=="membersList":
               try:
                #print('handling memberlist')
                receive =  client.recv(int(m[11:]))
                listobj=pickle.loads(receive)
                memberslist=listobj["0"]
                #print("membersList: 1"+memberslist)
               except Exception as e:
                   print('inside memembers list' + str(e))
            elif m=="groupdead":
                groupdead=True
            elif m[0:9]=="memberadd":
               try:
                addobj=pickle.loads(client.recv(int(m[9:])))
                memberslist.append(addobj['name'])
                clientmessageList.append({
                     'colour':"#223344",
                     'name':"ChatBot",
                     'message': addobj['message']
                })
               except Exception as e:
                   print('inside member add' + str(e))
            elif m[0:10]=="membergone":
                try:
                 recvobj=pickle.loads(client.recv(int(m[10:])))
                 member=recvobj["person"]
                 memberslist.remove(member)
                 clientmessageList.append({
                     "name":"ChatBot",
                     "colour":"#223344",
                     "message":recvobj["message"],
                 })
                except Exception as e:
                    print('inside membergone '+str(e))
            elif m[0:11]=="oldmessages":
               try:
                print(m[11:])
                gotit = client.recv(int(m[11:]))
                print(gotit)
                oldmessages={}
                oldmessages=pickle.loads(gotit)
                #print(oldmessages)
                clientmessageList=copy.deepcopy(oldmessages["0"])
               except Exception as e:
                   print('inside old messages' + str(e))
            
            elif m[0:10]=="newmessage":
               try:
                newmessage={}
                gotnew= client.recv(int(m[10:]))
                newmessage=pickle.loads(gotnew)
                print(newmessage)
                clientmessageList.append(copy.deepcopy(newmessage))   #{"colour":value , "name": value, "message": value }
               except Exception as e:
                   print('inside new message' + str(e))
        except Exception as e:
           print("Exception occured in receive:(client socket disc....) "+str(e))
           break

def return_details():
    global details
    print("details: "+str(details))
    return details

def makeNone():
    global groupfull,result
    result=None
    groupfull=None

def return_groupdead():
    global groupdead
    return groupdead
    
def set_group_dead():
    global groupdead
    groupdead=None

def return_authenticate():
    global result
    print('from client side:' + str(result))
    return result

def return_groupfull():
    global groupfull
    print('from client side:' + str(groupfull))
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
  try:
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
  except Exception as e:
      print("Exception in return_message: "+str(e))



def sendName(username):
  try:
    global client,name
    name=username
    name2=username.encode('UTF-8')
    header=f"{len(name2):<{HEADER_SIZE}}".encode("UTF-8")
    client.send(header+name2)
  except Exception as e:
      print("Exception occured in sendName: "+str(e))

def sendGroups():
  try:
    #print('sendGroups')
    global client
    m="groups".encode('UTF-8')
    header=f"{len(m):<{HEADER_SIZE}}".encode("UTF-8")
    client.send(header+m)
  except Exception as e:
      print("Exception occured in sendGroups: "+str(e))

# def sendMembers():
#   try:
#     #print('sendMembers')
#     global client
#     m="members".encode('UTF-8')
#     header=f"{len(m):<{HEADER_SIZE}}".encode("UTF-8")
#     client.send(header+m)
#   except Exception as e:
#       print("Exception occured in sendMembers: "+str(e))

def sendMembersList():
    print("ntg left to do")

def sendCreate(s):
  try:
    print('sendCreate')
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
        'colour':"#223344",
        'name':"ChatBot",
        'message':"Welcome to your Crypto Chamber! Share Chamber Name and Code with your friends and have fun sharing secrets on crypto chamber!!"
    })
  except Exception as e:
      print("Exception occured in sendCreate: "+str(e))

def sendJoin(s):
  try:
    #print('sendJoin')
    #global client
    #client.send("join".encode('ASCII'))
    #client.send(s.encode('ASCII'))
    print('sent-join-request')
    m="join".encode('UTF-8')
    header=f"{len(m):<{HEADER_SIZE}}".encode("UTF-8")
    client.sendall(header+m)
    m=s.encode('UTF-8')
    header=f"{len(m):<{HEADER_SIZE}}".encode("UTF-8")
    client.sendall(header+m)
  except Exception as e:
      print("Exception occured in sendJoin: "+str(e))

def sendMessage(mess,colour):
  try:
    print('sendMessage')
    global client,name
    message="message"
    messagedict={
        "colour":colour,
        "message":mess,
        "name":name
    }
    messageobj=pickle.dumps(messagedict)
    print(messageobj)
    message=message+str(len(messageobj))
    message=message.encode('UTF-8')
    header=f"{len(message):<{HEADER_SIZE}}".encode('UTF-8')
    client.sendall(header+message)
    client.sendall(messageobj)
  except Exception as e:
      print("Exception occured in sendMessage: "+str(e))

def sendLogout(*args):
  try:
    print('sendlogout')
    global client,sentList,clientmessageList,sentList
    clientmessageList.clear()
    sentList.clear()
    memberslist.clear()
    m="QUIT".encode('UTF-8')
    header=f"{len(m):<{HEADER_SIZE}}".encode("UTF-8")
    client.sendall(header+m)
  except Exception as e:
      print("Exception occured in sendLogout: "+str(e))

def close():
   global client
   try: 
    m="QUIT".encode('UTF-8')
    header=f"{len(m):<{HEADER_SIZE}}".encode("UTF-8")
    client.sendall(header+m)         
   except Exception as e:
      print("Exception occured in sendLogout: "+str(e)) 



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
groupdead=None
#Host=input("Enter the host name: ")
#Port=int(input("Enter the port number: "))
#Host="34.227.91.249"
def client_initialize():
    global client
    client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    Host="127.0.0.1"
    Port=8000
    #Host="52.204.124.224"
    #Port=8000
    client.connect((Host,Port))
    rthread=Thread(target=receive)
    rthread.start()


