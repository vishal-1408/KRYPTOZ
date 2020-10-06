
from threading import Thread
import socket
import sched 
import time

def accept():
    while 1:
        client_socket,client_addr = server_socket.accept()        #threads are just created for making blocks of code execute parallely! like accepting the connections and handling clients all these work in parallel
        print("A client has been connected to the server")
        Thread(target=initialize,args=(client_socket,)).start()
       # Thread(target=details,args=(client_socket,)).start()


def details(c):
    global groupinfo
    m="details!!!!!separator!!!!!"
    sep='*****seperator*****'
    for x,y  in groupinfo.items():
        m+=x+sep+y[0]+sep+str(y[1])+sep+str(y[2])+sep+" ".join([str(x) for x in y[3]])+"!!!!!separator!!!!!"
        #print(y)
    m=m.encode("ASCII")
    c.sendall(m)
    #print(m)
    return 1    
#"details;groupname,grouppassword,name1,name2,name3...;groupname,..."


def initialize(c):
    global clientinfo
    try:
        name=c.recv(1024).decode('ASCII')
        #print(name)
        clientinfo[c]=[name]
        d=1
        print("initialize")
        while(d):
            #print('while loop')
            m=c.recv(1024).decode('ASCII')
            #print(m)
            if(m=="groups"): #Gui part should send a message,
                d=details(c)
            elif(m=="create"):
                d=create(c)
            elif(m=="join"):
                d=join(c)
            elif(m=="QUIT"):
                c.send("Bye".encode("ASCII"))
                c.close()
                break
    except Exception as e:
        print(e)
        print("client socket closed")
        c.close()



def create(c):
    global clientinfo, groupinfo,eventslist
    try:
        print("create")
        string=c.recv(1024).decode("ASCII")
        list1=string.split("*****seperator*****")
        groupinfo[list1[0]]=[list1[1],int(list1[2]),list1[3],[clientinfo[c][0]]]            #groupinfo=[password,limit,groupcode,[]]
        clientinfo[c].append(list1[0])
        eventslist[list1[0]]=[]
        #print(clientinfo)
        #print(groupinfo)
        Thread(target=handling_the_client,args=(c,)).start()
        return 0      #return 0 once handling clients is done!
    except Exception as e:
        print("client socket closed")
        print(e+"inside create")
        clientinfo.remove(clientinfo[c])
        c.close()
        return 0


def join(c):
    e=1
    print("join")
    global clientinfo, groupinfo,eventslist,scheduler
    while e:
            #print(groupinfo)
            sep='*****seperator*****'
            string=c.recv(1024).decode("ASCII")
            name=string.split(sep)[0]
            #print(name)
            password=string.split(sep)[1]
            #print(password)
            grouppassword=groupinfo[name][0]
            #print(grouppassword + "\t" + password)
            if len(groupinfo[name][3])<(groupinfo[name][1]):
                if grouppassword==password:
                    c.sendall("$$auth$$t".encode("ASCII"))
                    for x in eventslist[name]:
                        if x:
                             print(x)
                             scheduler.cancel(x)
                             eventslist[name].remove(x)

                    #print(groupinfo)
                   # print(clientinfo)
                    groupinfo[name][3].append(clientinfo[c][0])
                    #print(groupinfo)
                    clientinfo[c].append(name)
                    Thread(target=handling_the_client,args=(c,)).start()           #//un comment it , when the chatting window is done!
                    return 0
                elif password!=grouppassword:
                    c.send("$$auth$$f".encode("ASCII"))
                    return 1                                                     #return 0 once handling clients is done!
            else:
                c.send("$$auth$$g")
                return 1




def handling_the_client(client):
    print("hanfdling client")
    global clientinfo, groupinfo
    # message=clientinfo[client][0]+" has joined the room!"
    # broadcast(message,"chatbot",client)
    # m="Welcome "+clientinfo[client][0]+"\nYou can enter a message and click enter and\nif you want to exit the app, please enter QUIT"
    # client.send(m.encode("ASCII"))
    while 1:
        received=client.recv(1024).decode('ASCII')
        print(received+" by "+clientinfo[client][0])
        if not received=="QUIT":
            broadcast(received,clientinfo[client][0],client)
        else:
            if len(groupinfo[clientinfo[client][1]][3])==1:
                groupinfo[clientinfo[client][1]][3].remove(clientinfo[client][0])
                group_name = clientinfo[client].pop()
                #client.close()
                #print(groupinfo)
                Thread(target=scheduling,args=(group_name,)).start()
                Thread(target=joinorcreate,args=(client,)).start()
                break
            else:
                #print("i removed it")
                groupinfo[clientinfo[client][1]][3].remove(clientinfo[client][0])
                clientinfo[client].pop()
                Thread(target=joinorcreate,args=(client,)).start()
                break
scheduler = None

def scheduling(group_name):
    global eventslist,scheduler
    print('clock')
    print(groupinfo)
    scheduler = sched.scheduler(time. time, time.sleep)
    e1 = scheduler.enter(7, 1, checkgroup,(group_name,))
    eventslist[group_name].append(e1)
    print(eventslist)
    scheduler.run()
    print('after clock')

def checkgroup(group_name):
    print('called')
    global clientinfo, groupinfo
    if len(groupinfo[group_name][3])==0:
        groupinfo.pop(group_name)
    #print(str(groupinfo)+'from check_groupasdfasdfasdfasdffasdfasdfasdfasdfasdfasdfasdfasdf!!!!!!!!!!!@@@@@@@@@###')


def joinorcreate(c):
    global clientinfo, groupinfo, scheduler
    try:
        d=1
        while(d):
            m=c.recv(1024).decode('ASCII')
            #print(m)
            if(m=="groups"): #Gui part should send a message,
                d=details(c)
            elif(m=="create"):
                d=create(c)
            elif(m=="join"):
                d=join(c)
            elif(m=="QUIT"):
                c.send("Bye".encode("ASCII"))
            # print("test")
                c.close()
                break
    except Exception as e:
        print("client socket closed")
        print(e)
        c.close()


def broadcast(message,name,client="",group=""):
    global clientinfo, groupinfo
    if not client=="":
        room=clientinfo[client][1]
        clients=groupinfo[room][1]
        if name=="chatbot":
            for x in clients:
                if not x==client:
                    m=name+" : "+message
                    m=m.encode("ASCII")
                    x.send(m)
        else:
            for x in clients:
                if not x==clients:
                    m=name+" : "+message
                    m=m.encode("ASCII")
                    x.send(m)
    else:
        clients=groupinfo[group][1]
        for x in clients:
             m=name+" : "+message
             m=m.encode("ASCII")
             x.send(m)



clientinfo={}
groupinfo={}
eventslist={}

Host=""
port=8000
server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

server_socket.bind((Host,port))
print(Host)


if __name__ == "__main__":
    server_socket.listen(10)
    print("Socket is listening for sockets!!")
    main_thread=Thread(target=accept)
    main_thread.start() #starts the thread
    main_thread.join() #blocks the code here till the main_threads execution doesn't end!
    server_socket.close()
