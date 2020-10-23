
from threading import Thread
import socket
import sched 
import time
import pickle
import copy
import random

HEADER_SIZE=10
def accept():
    while 1:
        client_socket,client_addr = server_socket.accept()        #threads are just created for making blocks of code execute parallely! like accepting the connections and handling clients all these work in parallel
        print("A client has been connected to the server")
        Thread(target=initialize,args=(client_socket,True)).start()


def details(c):
    try:
        #print("details")
        global groupinfo
        groupobject={}
        for x,y in groupinfo.items():
            groupobject[x]=list([y[1],y[2],len(y[3]),y[6]])
        messageobj=pickle.dumps(groupobject)
        message="details"+str(len(messageobj))
        message=message.encode('UTF-8')
        c.sendall(f"{len(message):<{HEADER_SIZE}}".encode('UTF-8')+message)
        c.sendall(messageobj)
        return 1
    except Exception as e:
        print("Exception occured in ddetails: "+str(e))



# def members(c):
#     global groupinfo,clientinfo
#     sep='*****seperator*****'
#     m="$$$length$$$"+"!!!!!separator!!!!!"

#     for x,y  in groupinfo.items():
#         m+=x+sep+str(len(y[3]))+"!!!!!separator!!!!!"
#     #print("from server, this is m"+ str(m))
#     m=m.encode("ASCII")
#     c.sendall(m)
#     return 1

def initialize(c,check):
    global clientinfo
    try:
        if check==True:
           obj_len=c.recv(HEADER_SIZE).decode('UTF-8')
          # print("messagelength"+mess_len)
           obj=c.recv(int(obj_len))
           loadedObj=pickle.loads(obj)
           name=loadedObj['name']
           print("initialize: "+name)
           clientinfo[c]=[name]
           clientinfo[c].append(loadedObj['publickey'])
        else:
            print("logged out : ")
        d=1
        while(d):
            header=c.recv(HEADER_SIZE).decode('UTF-8')
            m=c.recv(int(header)).decode('UTF-8')
            #print("MESSAGE AT INITIALIZE:"+m)
            if(m=="groups"): #Gui part should send a message,
                #print("groups2")
                d=details(c)
                #print("groups3")
            elif(m=="create"):
                d=create(c)
            elif(m=="join"):
                d=join(c)
            elif(m=="QUIT"):
                m="BYE".encode('UTF-8')
                header=f"{len(m):<{HEADER_SIZE}}".encode('UTF-8')
                c.sendall(header+m)
                c.close()
                break
    except Exception as e:
        if check==True:
            print("exception in initialize: "+str(e))
        else:
            print("exception after logging out: "+str(e))
            cl=clientinfo.pop(c)
            cl.close()



def create(c):
    global clientinfo, groupinfo,eventslist,groupMessages,groupencSenderkeys
    try:
        print("create")
        length=c.recv(HEADER_SIZE).decode("UTF-8")
        string=c.recv(int(length)).decode('UTF-8')
        list1=string.split("*****seperator*****")
        print(list1)
        if list1[1]=="":
         groupinfo[list1[0]+list1[3]]=[list1[1],int(list1[2]),len(list1[0]),[clientinfo[c][0]],[c],{clientinfo[c][0]:clientinfo[c][1]},False]            #groupinfo=[password,limit,groupcode,[],[]]
        else:
         groupinfo[list1[0]+list1[3]]=[list1[1],int(list1[2]),len(list1[0]),[clientinfo[c][0]],[c],{clientinfo[c][0]:clientinfo[c][1]},True]            #groupinfo=[password,limit,groupcode,[],[]]
        groupMessages[list1[0]+list1[3]]=[]
        clientinfo[c].append(list1[0]+list1[3])
        eventslist[list1[0]+list1[3]]=[]
        groupencSenderkeys[list1[0]+list1[3]]={}
        groupencSenderkeys[list1[0]+list1[3]][clientinfo[c][0]]={}
        #print(clientinfo)
        #print(groupinfo)
        Thread(target=handling_the_client,args=(c,)).start()
        return 0      #return 0 once handling clients is done!
    except Exception as e:
        print("exception in create: "+str(e))
       # clientinfo.remove(clientinfo[c])
        c.close()
        return 0


def join(c):
    e=1
    print("join")
    sep='*****seperator*****'
    global clientinfo, groupinfo,eventslist,scheduler,groupMessages,groupencSenderkeys
    try:
        while e:
            #print(groupinfo)
          length=c.recv(HEADER_SIZE).decode('UTF-8')
          string=c.recv(int(length)).decode('UTF-8')
          name=string.split(sep)[0]   #name of the group should be sent concat with code!!
          #print("name: "+name)
          password=string.split(sep)[1]
          #print("password:"+password)
          grouppassword=groupinfo[name][0]
          #print(grouppassword + "\t" + password)
          obj={}
          message="auth"
          if name in groupinfo.keys():
             if len(groupinfo[name][3])<(groupinfo[name][1]):
                #print("inside")
                if grouppassword==password or not groupinfo[name][6]:
                    obj['result']=True
                    obj['groupfull']=False
                    messageobj=pickle.dumps(obj)
                    message=message+str(len(messageobj))
                    message=message.encode('UTF-8')
                    header=f'{len(message):<{HEADER_SIZE}}'.encode('UTF-8')
                    c.sendall(header+message)
                    c.sendall(messageobj)
                    #print("Sent succeslly")
                    for x in eventslist[name]:
                        if x:
                             scheduler.cancel(x)
                             eventslist[name].remove(x)

                    #print(groupinfo)
                   # print(clientinfo)
                    groupinfo[name][3].append(clientinfo[c][0])
                    groupinfo[name][4].append(c)
                    groupinfo[name][5][clientinfo[c][0]]=clientinfo[c][1]

                    #print("joined:"+str(groupinfo))
                    clientinfo[c].append(name)
                    
                    # groupMessages[name].append({
                    #     "colour":"#223344",
                    #     'message':"{} has joined the chamber!".format(clientinfo[c][0]),
                    #     "name":"ChatBot"
                    # })
                    sendAllmemberslist(name,c)
                    if len(groupinfo[name][3])!=1:
                      
                      length=c.recv(HEADER_SIZE).decode('UTF-8')
                      string=c.recv(int(length)).decode('UTF-8')

                      length123=c.recv(HEADER_SIZE).decode('UTF-8')

                      message=c.recv(int(length123)).decode('UTF-8')

                      rawobj=c.recv(int(message[4:]))
                      eSKeys=pickle.loads(rawobj)

                      groupencSenderkeys[name][clientinfo[c][0]]=eSKeys

                    
                      broadcasteveryone(name,c,clientinfo[c][1])
                      print("broadcast done")
                      d=1
                      keysobject={}
                      try:
                       while(d):
                        dictkeys=groupencSenderkeys[name].keys()
                        l=0
                        for x in dictkeys:
                          #print("loop:"+str(x))
                          if x!=clientinfo[c][0]:
                            print("loop2 :"+str(groupencSenderkeys[name][x].keys()))
                            if clientinfo[c][0] not in groupencSenderkeys[name][x].keys():
                                l=1
                            else:
                                keysobject[x]=groupencSenderkeys[name][x][clientinfo[c][0]]
                                print("in loop:"+str(keysobject))

                        d=l
                      except Exception as e:
                       print(e)
                      print("got the senderkeys encrypted of all other users:"+str(keysobject))
                      pickledobj=pickle.dumps(keysobject)
                      m=("memeberskeys"+str(len(pickledobj))).encode('UTF-8')
                      header=f"{len(m):<{HEADER_SIZE}}".encode('UTF-8')
                      c.sendall(header+m)
                      c.sendall(pickledobj)
                      print(groupMessages[name])
                      while(len(groupMessages[name])==0):
                        #print("waiting!!!!")
                        pass
                      print("old messages are being sent!!!")
                      messagearray=copy.deepcopy(groupMessages[name])
                      pickledmessagearray=pickle.dumps(messagearray)
                      message1=("oldmessages"+str(len(pickledmessagearray))).encode('UTF-8')
                      header2=f"{len(message1):{HEADER_SIZE}}".encode('UTF-8')
                      c.sendall(header2+message1)
                      c.sendall(pickledmessagearray)
                      print("sent!!! :"+str(messagearray))
                      groupMessages[name]=[]
                    else:
                      groupencSenderkeys[name][clientinfo[c][0]]={}
                    #he can go to handling client!!!!!
                    Thread(target=handling_the_client,args=(c,)).start()           #//un comment it , when the chatting window is done!
                    return 0
                elif password!=grouppassword:
                    obj['result']=False
                    obj['groupfull']=False
                                               #return 0 once handling clients is done!
             else:
                    obj['result']=False
                    obj['groupfull']=True
             messageobj=pickle.dumps(obj)
             message=message+str(len(messageobj))
             message=message.encode('UTF-8')
             header=f'{len(message):<{HEADER_SIZE}}'.encode('UTF-8')
             c.sendall(header+message)
             c.sendall(messageobj)
             return 1
          else:
             return 1
    except Exception as e:
             message="groupdead"
             message=message.encode('UTF-8')
             header=f'{len(message):<{HEADER_SIZE}}'.encode('UTF-8')
             c.sendall(header+message)
             print("Exception in join: "+str(e))
             return 1


def sendAllmemberslist(name,c):
    print("send all members list")
    try:
        message="membersList"
        obj={}
        obj["0"]=groupinfo[name][3]
        obj["1"]=groupinfo[name][5]
        #print("memberslist"+str(obj["0"]))
        messageobj=pickle.dumps(obj)
        message=message+str(len(messageobj))
        message=message.encode('UTF-8')
        header=f"{len(message):<{HEADER_SIZE}}".encode('UTF-8')
        c.sendall(header+message)
        c.sendall(messageobj)
    except Exception as e:
        print("Exception occured in sendAllmembersList: "+str(e))
        return
    

def broadcasteveryone(gname,client,pkey):
    try:
        global clientinfo,groupinfo,groupencSenderkeys
        i=0
        index=random.randint(0,len(groupinfo[gname][3])-2)
        for x in groupinfo[gname][4]:
           #print("sending!!!")
           if x!=client:
            if index==i:
                check=True
            else:
                check=False
            message="memberadd"
            addobj={'name':clientinfo[client][0],
            'message': '{} has joined the chamber!'.format(clientinfo[client][0]),
            'publickey':pkey,'encSkey':groupencSenderkeys[gname][clientinfo[client][0]][groupinfo[gname][3][i]],
            'check':check
            }

            messageobj=pickle.dumps(addobj)
            message=message+str(len(messageobj))
            message=message.encode('UTF-8')
            header=f"{len(message):<{HEADER_SIZE}}".encode('UTF-8')
            x.sendall(header+message)
            x.sendall(messageobj)
            i+=1
    except Exception as e:
        print("Exception occured in broadcast everyone: "+str(e))
        return
           



def sendAllMessages(groupname,c):
    try:
        global groupMessages
        oldmessages={'0':groupMessages[groupname]}
        #print("oldmessages: "+str(oldmessages))
        messageobj=pickle.dumps(oldmessages)
        message="oldmessages"
        message=message+str(len(messageobj))
        message=message.encode('UTF-8')
        header=f"{len(message):<{HEADER_SIZE}}".encode('UTF-8')
        c.sendall(header+message)
        c.sendall(messageobj)
    except Exception as e:
        print("Exception occured in sendAllMessages: "+str(e))
        return

"""
{
 'A':{
     'B':'senderkey',
     'C':'senderkey',
 }
}

***** group keys length==groupmemebrslength****




"""
def handling_the_client(client):
    try:
        print("handling client")
        global clientinfo, groupinfo,groupMessages,groupencSenderkeys
        while 1:
             length=client.recv(HEADER_SIZE).decode('UTF-8')
             print(length)
             message=client.recv(int(length)).decode('UTF-8')
             print("received in handling client:"+message)
            # if message[0:9]=="publickey":
             #    catchPublicky(client,groupinfo,int(message[9:]))
             if message[0:7]=="message":
                broadcast(clientinfo[client][0],client,groupinfo[clientinfo[client][2]][4],int(message[7:]),True)
             elif message[0:6]=="append":
                 rawarray=client.recv(int(message[6:]))
                 array=pickle.loads(rawarray)
                 groupencSenderkeys[clientinfo[client][2]][clientinfo[client][0]]={}
                 groupencSenderkeys[clientinfo[client][2]][clientinfo[client][0]][array[0]]=array[1]
                # print(groupencSenderkeys)
             elif message[0:4]=="blah":
                 recveied=client.recv(int(message[0:4]))
             elif message[0:6]=="redone":
                 checkAvailable(client,int(message[6:]))
             elif message[0:11]=="oldmessages":
                 populateOldMessages(client,int(message[11:]))
             elif message=="QUIT":
                if len(groupinfo[clientinfo[client][2]][3])==1:
                    group_name=clientinfo[client][2]
                    leavingGroup(client)
                    # groupinfo[clientinfo[client][2]][3].remove(clientinfo[client][0])
                    # groupinfo[clientinfo[client][2]][4].remove(client)
                    # groupinfo[clientinfo[client][2]][5].pop(clientinfo[client][0])
                    # group_name = clientinfo[client].pop()
                    # groupencSenderkeys[group_name].pop(clientinfo[client[0]])
                    #print("group details:"+str(groupinfo[group_name]))
                    Thread(target=scheduling,args=(group_name,)).start()
                    Thread(target=initialize,args=(client,False)).start()
                    break
                else:
                    broadcast(clientinfo[client][0],client,groupinfo[clientinfo[client][2]][4],"",False)
                    leavingGroup(client)
                    # groupinfo[clientinfo[client][2]][3].remove(clientinfo[client][0])
                    # groupinfo[clientinfo[client][2]][4].remove(client)
                    # groupinfo[clientinfo[client][2]][5].pop(clientinfo[client][0])
                    # groupencSenderkeys[clientinfo[client][2]].pop(clientinfo[client[0]]
                    Thread(target=initialize,args=(client,False)).start()
                    break
    except Exception as e:
        print("Exception occured in handling client: "+str(e))
        return

def populateOldMessages(c,length):
    global groupMessages,clientinfo
    bytesarr=c.recv(length)
    loadedarr=pickle.loads(bytesarr)
    loadedarr.insert(0,clientinfo[c][0])
    groupMessages[clientinfo[c][2]]=copy.deepcopy(loadedarr) #1st index is the anme of client sending it!!

    print("messages populated!!!!")

def leavingGroup(client):
   try:
     global clientinfo,groupinfo,groupencSenderkeys
     groupinfo[clientinfo[client][2]][3].remove(clientinfo[client][0])
     groupinfo[clientinfo[client][2]][4].remove(client)
     groupinfo[clientinfo[client][2]][5].pop(clientinfo[client][0])
     groupencSenderkeys[clientinfo[client][2]].pop(clientinfo[client][0])
     group_name=clientinfo[client].pop()
     for x in groupinfo[group_name][3]:
          groupencSenderkeys[group_name][x].clear() # clearing out the dictionary of every single person!!!!
   except Exception as e:
       print("Exception occured in leaving group: "+str(e))
     

def checkAvailable(c,length):
  global groupencSenderkeys,clientinfo
  try:  
    dumpedobj=c.recv(length)
    pickledobj=pickle.loads(dumpedobj)
    gname=clientinfo[c][2]
    clientname=clientinfo[c][0]
    groupencSenderkeys[gname][clientname]=pickledobj
    d=1
    keysobject={}
    try:
      while(d):
        dictkeys=groupencSenderkeys[gname].keys()
        l=0
        for x in dictkeys:
            #print("loop:"+str(x))
            if x!=clientname:
                #print("loop2 :"+str(groupencSenderkeys[name][x].keys()))
                if clientname not in groupencSenderkeys[gname][x].keys():
                    l=1
                else:
                    keysobject[x]=groupencSenderkeys[gname][x][clientname]
                    #print("in loop:"+str(keysobject))
        d=l
    except Exception as e:
        print("exception inside checkavail while:"+str(e))
    #print("keysobject:"+str(keysobject))
    pickledobj=pickle.dumps(keysobject)
    m=("memeberskeys"+str(len(pickledobj))).encode('UTF-8')
    header=f"{len(m):<{HEADER_SIZE}}".encode('UTF-8')
    c.sendall(header+m)
    c.sendall(pickledobj) 
  except Exception as e:
       print("HEY exception in checkavail"+str(e))
    



def broadcast(name,client,memberslist,length,check):
  try:
    global clientinfo,groupMessages
    if check==True:
        messageobj=client.recv(length)
        # newmessageobj["name"]=clientinfo[client][0]
        # print("broadcast: "+ str(newmessageobj))
        #groupMessages[clientinfo[client][2]].append(copy.deepcopy(newmessageobj))
        # messageobj=pickle.dumps(newmessageobj)
        message="newmessage"
    else:
        messageobj=pickle.dumps({
            "name":"ChatBot",
            "colour":"#223344",
            "message":"{} has left the chat".format(name),
            "person":name
        })
        # groupMessages[clientinfo[client][2]].append({
        #     "name":"ChatBot",
        #     "colour":"#223344",
        #     "message":"{} has left the chat".format(name)
        # })
        message="membergone"
    message=message+str(len(messageobj))

    message=message.encode('UTF-8')
    header=f"{len(message):<{HEADER_SIZE}}".encode('UTF-8')
    #print("memberlist:"+str(memberslist))
    for x in memberslist:
        if x!=client:
            x.sendall(header+message)
            x.sendall(messageobj)
    print("member broadcast done!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
  except Exception as e:
     print("Exception occured in broadcast: "+str(e))
     return



def scheduling(group_name):
 try:
    global eventslist,scheduler
    #print('clock')
    #print(groupinfo)
    scheduler = sched.scheduler(time. time, time.sleep)
    e1 = scheduler.enter(7, 1, checkgroup,(group_name,))
    eventslist[group_name].append(e1)
    #print(eventslist)
    scheduler.run()
    #print('after clock')
 except Exception as e:
    print("Exception occured in scheduling: "+str(e))
    return

def checkgroup(group_name):
  try:
    #print('called')
    global clientinfo, groupinfo
    if len(groupinfo[group_name][3])==0:
        groupinfo.pop(group_name)
        groupMessages.pop(group_name)
  except Exception as e:
    print("Exception occured in checkgroup: "+str(e))
    return



clientinfo={}
groupinfo={}
eventslist={}
groupMessages={}
groupencSenderkeys={}
scheduler = None

Host=""
port=8000
server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

server_socket.bind((Host,port))
#print(Host)


if __name__ == "__main__":
    server_socket.listen(50)
    print("Socket is listening for sockets!!")
    main_thread=Thread(target=accept)
    main_thread.start() #starts the thread
    main_thread.join() #blocks the code here till the main_threads execution doesn't end!
    server_socket.close()
