
from threading import Thread
import copy
import socket
import pickle
import random
from EncryptionHashing import *

HEADER_SIZE=10

def receive():
    global client
    global details, result,groupfull
    global members,memberslist,clientmessageList,name,groupdead,check
    global publickeys,decSenderKeys,clientsenderkey
    i=1
    #print('Function Started!!!!')
    while 1:
        try:
            length=client.recv(HEADER_SIZE).decode('UTF-8')
            #print("legnth: "+str(length))
            m=client.recv(int(length)).decode('UTF-8')
            #print("message:"+str(m))
            if m=="BYE":
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
                #print("object received:::::::::::::::::::::::::::::::::::::::::"+str(obj))
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
                publickeys=listobj["1"]
                generateSenderKeys(False)
                #print("membersList: 1"+memberslist)
               except Exception as e:
                   print('inside memembers list' + str(e))
            elif m=="groupdead":
                print('GroupDead received')
                groupdead=True
            elif m[0:12]=="memeberskeys":
                rawbytesobj=client.recv(int(m[12:]))
                pickledobj=pickle.loads(rawbytesobj)
                decSenderKeys=pickledobj
                print(decSenderKeys)
                print("EVERYTHING RECEIVED !!!!!")
                print(encSenderKeys)

            elif m[0:9]=="memberadd":
               try:
                addobj=pickle.loads(client.recv(int(m[9:])))
                memberslist.append(addobj['name'])
                clientmessageList.append({
                     'colour':"#223344",
                     'name':"ChatBot",
                     'message': addobj['message']
                })
                publickeys[addobj['name']]=addobj['publickey']
                decSenderKeys[addobj['name']]=addobj['encSkey']
                check=1
                generateSenderKey(addobj['name'])
                check=0
                """
                check=1
                func(pkey,name)
                func()--send the whole enckey{} to server!
                check=0

                """
               except Exception as e:
                   print('inside member add' + str(e))
            elif m[0:10]=="membergone":
                try:
                 recvobj=pickle.loads(client.recv(int(m[10:])))
                 member=recvobj["person"]
                 memberslist.remove(member)
                 publickeys.pop(recvobj["person"]) #removing the public key of the person!!!
                 clientmessageList.append({
                     "name":"ChatBot",
                     "colour":"#223344",
                     "message":recvobj["message"],
                 })
                 clientsenderkey=generate_AES_key() #changing the sender key!!!
                 generateSenderKeys(True)

                 """
                check=1
                func() generate new sender keys and enc sender keys for every memeber!
                func()--send the whole enckey{} to server!
                check=0
                
                """
                except Exception as e:
                    print('inside membergone '+str(e))
            elif m[0:11]=="oldmessages":
               try:
                #print(m[11:])
                gotit = client.recv(int(m[11:]))
                #print(gotit)
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
    #print("details: "+str(details))
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
    #print('from client side:' + str(result))
    return result

def return_groupfull():
    global groupfull
    #print('from client side:' + str(groupfull))
    return groupfull

def return_members():
    global members,details
    for x,y in details.items():
        members[x]=y[2]
    return members

def return_memeberslist():
    global memberslist
    #print(memberslist)
    return memberslist

def return_publickeys():
    global publickeys
    return publickeys

def return_message():
  try:
    global clientmessageList,sentList
    if len(sentList)==0:
        sentList=copy.deepcopy(clientmessageList)
        #print('a'+str(sentList))
        return sentList
    elif len(sentList)==len(clientmessageList):
        return []
    else:
        newMessages=clientmessageList[len(sentList):]
        for i in newMessages:
            sentList.append(i)
        #print('c'+str(newMessages))
        return newMessages
  except Exception as e:
      print("Exception in return_message: "+str(e))

def generateSenderKeys(check):
  try:
    #print("came")
    global publickeys,encSenderKeys,privatekey,clientsenderkey,name
    global client
    for x,y in publickeys.items():
      if x!=name:
        print("public keys:"+str(y))
        secretkey = generate_secret_key(privatekey,y) #y-publickkey of the user with which the secret key is generated
        encsenderkey = encryption(secretkey,clientsenderkey)
        encSenderKeys[x]=encsenderkey # {otheruser : encsenderkey}
    #print("encrypted dict: "+str(encSenderKeys))
    messsageobj=pickle.dumps(encSenderKeys)
    if check==False:
      message=("blah"+str(len(messsageobj))).encode('UTF-8')
    else:
      message=("redone"+str(len(messsageobj))).encode('UTF-8')
    #print("message: "+str(message))
    header=f"{len(message):<{HEADER_SIZE}}".encode('UTF-8')
    client.sendall(header+message)
    client.sendall(messsageobj)

    print("generate out !!!")
    print(encSenderKeys)
  except Exception as e:
      print(e)


def generateSenderKey(name):
  try:
    global encSenderKeys,publickeys,clientsenderkey,privatekey
    global client
    publickey=publickeys[name]
    secretkey=generate_secret_key(privatekey,publickey)
    encSenderKey=encryption(secretkey,clientsenderkey)
    encSenderKeys[name]=encSenderKey
    array=[name,encSenderKey]
    messagearray=pickle.dumps(array)
    m=("append"+str(len(messagearray))).encode('UTF-8')
    header=f"{len(m):<{HEADER_SIZE}}".encode('UTF-8')
    client.sendall(header+m)
    client.sendall(messagearray)
  except Exception as e:
      print(e)





"""
{
 "A":"key",
 "B":"key"
}



groupinfo[name][6][clientinfo[c][0]]=
a:
{
 b:senderkey of a encryptedusing b's public key,
 c:senderkeyofa,
}

b:{
  a:senderkeyofb,
  c:senderkeyofb,
}

"""







def sendName(username,pkey,prkey,senderkey):
  try:
    global client,name,publickeys,privatekey,clientsenderkey
    privatekey=prkey
    clientsenderkey=senderkey
    publickeys[username]=pkey
    name=username
    obj={
        'name':name,
        'publickey':pkey
    }
    dumpedobj=pickle.dumps(obj)
    #name2=username.encode('UTF-8')
    header=f"{len(dumpedobj):<{HEADER_SIZE}}".encode("UTF-8")
    client.sendall(header)
    client.sendall(dumpedobj)
  except Exception as e:
      print("Exception occured in sendName: "+str(e))

def sendGroups():
  try:
    print('sendGroups')
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
    print('sent-join-request')
    m="join".encode('UTF-8')
    header=f"{len(m):<{HEADER_SIZE}}".encode("UTF-8")
    client.sendall(header+m)
    m=s.encode('UTF-8')
    header=f"{len(m):<{HEADER_SIZE}}".encode("UTF-8")
    client.send(header+m)
    client.send(header+m)
    #print("sent!!!")
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
  global name,clientsenderkey
  try:
   if name is not '' :
    print('sendlogout')
    global client,sentList,clientmessageList,sentList,publickeys,encSenderKeys,decSenderKeys
    clientmessageList.clear()
    sentList.clear()
    memberslist.clear()
    publickeys.clear()
    encSenderKeys.clear()
    decSenderKeys.clear()
    clientsenderkey=generate_AES_key  #regenerating sender key !!! as he is leaving the group!
    encSenderKeys
    m="QUIT".encode('UTF-8')
    header=f"{len(m):<{HEADER_SIZE}}".encode("UTF-8")
    client.sendall(header+m)
    print("sent ")
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
name=''
groupname=None
groupdead=None
publickeys={}
encSenderKeys={} #keys encrypted by this client's private key!
decSenderKeys={} #keys of other ppl!! used for decrypting!
privatekey=None
clientsenderkey=None
check=0

#Host=input("Enter the host name: ")
#Port=int(input("Enter the port number: "))
#Host="34.227.91.249"
def client_initialize():
    global client
    client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    Host="127.0.0.1"
    Port=8000
    #Host="52.204.124.224"
   # Port=8000
    client.connect((Host,Port))
    rthread=Thread(target=receive)
    rthread.start()


