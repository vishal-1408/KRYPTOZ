
from threading import Thread
import socket
import sched 
import time
import pickle
import copy

HEADER_SIZE=10
def accept():
    while 1:
        client_socket,client_addr = server_socket.accept()        #threads are just created for making blocks of code execute parallely! like accepting the connections and handling clients all these work in parallel
        print("A client has been connected to the server")
        Thread(target=initialize,args=(client_socket,True)).start()


def details(c):
    try:
        print("details")
        global groupinfo
        groupobject={}
        for x,y in groupinfo.items():
            groupobject[x]=list([y[1],y[2],len(y[3])]) 
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
           mess_len=c.recv(HEADER_SIZE).decode('UTF-8')
          # print("messagelength"+mess_len)
           name=c.recv(int(mess_len)).decode('UTF-8')
           print("initialize: "+name)
           clientinfo[c]=[name]
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
                c.send("Bye".encode("ASCII"))
                c.close()
                break
    except Exception as e:
        if check==True:
            print("exception in initialize: "+str(e))
        else:
            print("exception after logging out: "+str(e))
            
        c.close()



def create(c):
    global clientinfo, groupinfo,eventslist,groupMessages
    try:
        print("create")
        length=c.recv(HEADER_SIZE).decode("UTF-8")
        string=c.recv(int(length)).decode('UTF-8')
        list1=string.split("*****seperator*****")
        print(list1)
        groupinfo[list1[0]+list1[3]]=[list1[1],int(list1[2]),len(list1[0]),[clientinfo[c][0]],[c]]            #groupinfo=[password,limit,groupcode,[],[]]
        groupMessages[list1[0]+list1[3]]=[]
        clientinfo[c].append(list1[0]+list1[3])
        eventslist[list1[0]+list1[3]]=[]
        #print(clientinfo)
        #print(groupinfo)
        Thread(target=handling_the_client,args=(c,)).start()
        return 0      #return 0 once handling clients is done!
    except Exception as e:
        print("exception in create: "+str(e))
        clientinfo.remove(clientinfo[c])
        c.close()
        return 0


def join(c):
    e=1
    print("join")
    sep='*****seperator*****'
    global clientinfo, groupinfo,eventslist,scheduler,groupMessages
    try:
        while e:
            #print(groupinfo)
          length=c.recv(HEADER_SIZE).decode("UTF-8")
          string=c.recv(int(length)).decode('UTF-8')
          name=string.split(sep)[0]   #name of the group should be sent concat with code!!
          print(name)
          password=string.split(sep)[1]
          print(password)
          grouppassword=groupinfo[name][0]
          print(grouppassword + "\t" + password)
          obj={}
          message="auth"
          if name in groupinfo.keys():
             if len(groupinfo[name][3])<(groupinfo[name][1]):
                print("insdie")
                if grouppassword==password:
                    obj['result']=True
                    obj['groupfull']=False
                    messageobj=pickle.dumps(obj)
                    message=message+str(len(messageobj))
                    message=message.encode('UTF-8')
                    header=f'{len(message):<{HEADER_SIZE}}'.encode('UTF-8')
                    c.sendall(header+message)
                    c.sendall(messageobj)
                    print("Sent succesylly")
                    for x in eventslist[name]:
                        if x:
                             scheduler.cancel(x)
                             eventslist[name].remove(x)

                    #print(groupinfo)
                   # print(clientinfo)
                    groupinfo[name][3].append(clientinfo[c][0])
                    groupinfo[name][4].append(c)
                    print("joined:"+str(groupinfo))
                    clientinfo[c].append(name)
                    
                    groupMessages[name].append({
                        "colour":"#223344",
                        'message':"{} has joined the chamber!".format(clientinfo[c][0]),
                        "name":"ChatBot"
                    })

                    sendAllmemberslist(name,c)

                    sendAllMessages(name,c)
                   
                    broadcasteveryone(name,c)
                    
                    

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
        print("memberslist"+str(obj["0"]))
        messageobj=pickle.dumps(obj)
        message=message+str(len(messageobj))
        message=message.encode('UTF-8')
        header=f"{len(message):<{HEADER_SIZE}}".encode('UTF-8')
        c.sendall(header+message)
        c.sendall(messageobj)
    except Exception as e:
        print("Exception occured in sendAllmembersList: "+str(e))
        return
    

def broadcasteveryone(gname,client):
    try:
        global clientinfo,groupinfo
        message="memberadd"
        addobj={'name':clientinfo[client][0], 'message': '{} has joined the chamber!'.format(clientinfo[client][0])}
        messageobj=pickle.dumps(addobj)
        message=message+str(len(messageobj))
        message=message.encode('UTF-8')
        header=f"{len(message):<{HEADER_SIZE}}".encode('UTF-8')
        for x in groupinfo[gname][4]:
           if x!=client:
            x.sendall(header+message)
            x.sendall(messageobj)
    except Exception as e:
        print("Exception occured in broadcast everyone: "+str(e))
        return
           



def sendAllMessages(groupname,c):
    try:
        global groupMessages
        oldmessages={'0':groupMessages[groupname]}
        print("oldmessages: "+str(oldmessages))
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

    
    
    

       

# def membersList(client,grouplist):
#     sep='*****seperator*****'                                                    #groupinfo=[password,limit,groupcode,[],[]]
#     groupmembers="$$memlist$$"+sep
#     for x in grouplist[3]:
#         groupmembers+=x+sep
#     #print(groupmembers)
#     client.sendall(groupmembers.encode("ascii"))





def handling_the_client(client):
    try:
        print("handling client")
        global clientinfo, groupinfo,groupMessages
        while 1:
             length=client.recv(HEADER_SIZE).decode('UTF-8')
             #print(length)
             message=client.recv(int(length)).decode('UTF-8')
             #print(message)
             if message[0:7]=="message":
                broadcast(clientinfo[client][0],client,groupinfo[clientinfo[client][1]][4],int(message[7:]),True)
             elif message=="QUIT":
                if len(groupinfo[clientinfo[client][1]][3])==1:
                    groupinfo[clientinfo[client][1]][3].remove(clientinfo[client][0])
                    groupinfo[clientinfo[client][1]][4].remove(client)
                    group_name = clientinfo[client].pop()
                    print("group details:"+str(groupinfo[group_name]))
                    Thread(target=scheduling,args=(group_name,)).start()
                    Thread(target=initialize,args=(client,False)).start()
                    break
                else:
                    broadcast(clientinfo[client][0],client,groupinfo[clientinfo[client][1]][4],"",False)
                    groupinfo[clientinfo[client][1]][3].remove(clientinfo[client][0])
                    groupinfo[clientinfo[client][1]][4].remove(client)
                    clientinfo[client].pop()
                    Thread(target=initialize,args=(client,False)).start()
                    break
    except Exception as e:
        print("Exception occured in handling client: "+str(e))
        return

def broadcast(name,client,memberslist,length,check):
  try:
    global clientinfo,groupMessages
    if check==True:
        newmessageobj=pickle.loads(client.recv(length))
        #print("broadcast: "+ str(newmessageobj))
        groupMessages[clientinfo[client][1]].append(copy.deepcopy(newmessageobj))
        messageobj=pickle.dumps(newmessageobj)
        message="newmessage"
    else:
        messageobj=pickle.dumps({
            "name":"ChatBot",
            "colour":"#223344",
            "message":"{} has left the chat".format(name),
            "person":name
        })
        groupMessages[clientinfo[client][1]].append({
            "name":"ChatBot",
            "colour":"#223344",
            "message":"{} has left the chat".format(name)
        })
        message="membergone"
    message=message+str(len(messageobj))
    message=message.encode('UTF-8')
    header=f"{len(message):<{HEADER_SIZE}}".encode('UTF-8')
    print("memberlist:"+str(memberslist))
    for x in memberslist:
        if x!=client:
            x.sendall(header+message)
            x.sendall(messageobj)
    print("member broadcast done!")
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
    #print(str(groupinfo)+'from check_groupasdfasdfasdfasdffasdfasdfasdfasdfasdfasdfasdfasdf!!!!!!!!!!!@@@@@@@@@###')
  except Exception as e:
    print("Exception occured in checkgroup: "+str(e))
    return

# def joinorcreate(c):
#     global clientinfo, groupinfo, scheduler
#     try:
#         d=1
#         while(d):
#             m=c.recv(1024).decode('ASCII')
#             #print(m)
#             if(m=="groups"): #Gui part should send a message,
#                 d=details(c)
#             elif(m=="members"):
#                 d=members(c)
#             elif(m=="create"):
#                 d=create(c)
#             elif(m=="join"):
#                 d=join(c)
#             elif(m=="QUIT"):
#                 c.send("Bye".encode("ASCII"))
#             # print("test")
#                 c.close()
#                 break
#     except Exception as e:
#         print("client socket closed")
#         print(e)
#         c.close()



clientinfo={}
groupinfo={}
eventslist={}
groupMessages={}
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
