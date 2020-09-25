
from threading import Thread
import socket


def accept():
    while 1:
        client_socket,client_addr = server_socket.accept()        #threads are just created for making blocks of code execute parallely! like accepting the connections and handling clients all these work in parallel
        print("A client has been connected to the server")
        Thread(target=initialize,args=(client_socket,)).start()
       # Thread(target=details,args=(client_socket,)).start()

def details(c):
    print("came2")
    m="details;"
    for x,y  in groupinfo.items():
      m+=str(x)+","+str(y[0])+","+" ".join([str(x) for x in y[1]])+";"
      m=m.encode("ASCII")
      c.sendall(m)
    return 1    
"details;groupname,grouppassword,name1,name2,name3...;groupname,..."
            
        
        
        

def initialize(c):
        print("came")
        try:
         """client_socket.send("Please enter your name and click enter".encode("ASCII"))
         message = client_socket.recv(1024)
         message=message.decode('ASCII')
         print(message)
         if message=="QUIT":
            m="Bye! Hope you come back soon..."
            m=m.encode("ASCII")
            client_socket.send(m)
            client_socket.close()
            return 0
         clientinfo[client_socket]=[message]
         d=1
         while(d):
           client_socket.send("Type 1 for creating a group and 2 for joining a group and click enter".encode("ASCII"))
           c=client_socket.recv(1024).decode("ASCII")
           if c=="QUIT":
               m="Bye! Hope you come back soon..."
               m=m.encode("ASCII")
               client_socket.send(m)
               client_socket.close()
               return 0
           if c=="1":
               d=create(client_socket)
           elif c=="2":
               d=join(client_socket)"""
    

         name=c.recv(1024).decode('ASCII')
         clientinfo[c]=[name]
         d=1
         while(d):
             m=c.recv(1024).decode('ASCII')
             if(m=="groups"): #Gui part should send a message,
                 d=details(c)
             elif(m=="create"):
                 d=create(c)
             elif(m=="join"):
                 d=join(c)
             elif(m=="QUIT"):
                 c.close()
                 d=0
             
        
             
        except Exception as e:
            print("client socket closed")
            c.close()



def create(c):
    try:
     print("create")
     """if(len(groupinfo)!=0):
        m="The foll. group names are not available:\n"
        for x in groupinfo:
            m+=(str(x)+"\n")
        c.send(m.encode("ASCII"))"""
     string=c.recv(1024).decode("ASCII")
     list1=string.split(",") 
     groupinfo[list1[0]]=[list1[1],[c]]
     clientinfo[c].append(name)
     Thread(target=handling_the_client,args=(c,)).start()
     return 0
    except Exception as e:
        print("client socket closed")
        clientinfo.remove(clientinfo[client_socket])
        return 0
        

def join(c):
    e=1
    while e:
        if not len(groupinfo)==0:
            """ m="The foll. groups are available:"
            for x in groupinfo:
                m+=(str(x)+"\n")
            m+="Please enter the group name, you want to join: "
            c.send(m.encode("ASCII"))"""
            name=c.recv(1024).decode("ASCII")
            if name not in groupinfo:
               m="Group doesn't exist, Enter 1 to try again and 0 to go to main menu: "
               c.send(m.encode("ASCII"))
               res=c.recv(1024).decode("ASCII")
               if res=="1":
                continue
               elif res=="0":
                return 1
            else:
               m="Enter the password of the group: "
               c.send(m.encode("ASCII"))
               p=c.recv(1024).decode("ASCII")
               cpass=groupinfo[name][0]
               if p==cpass:
                 if len(groupinfo[name][1])<2:
                    m="Welcome to "+name
                    c.sendall(m.encode("ASCII"))
                    groupinfo[name][1].append(c)
                    clientinfo[c].append(name)
                    Thread(target=handling_the_client,args=(c,)).start()
                    return 0

                 else:
                  m="Group is full, Enter 1 to try again and 0 for the main menu"
                  c.send(m.encode("ASCII"))
                  res=c.recv(1024)
                  if res=="0":
                    return 1
                  else:
                    continue
               elif p!=cpass:
                m="Entered password is incorrect,Enter 1 to try again and 0 for the main menu"
                c.send(m.encode("ASCII"))
                res=c.recv(1024).decode("ASCII")
                if res=="0":
                    return 1
                else:
                    continue
        else:
            m="No groups are available , Redirecting you to the main menu...".encode("ASCII")
            c.send(m)
            return 1
            

    
        

def handling_the_client(client):
    message=clientinfo[client][0]+" has joined the room!"
    broadcast(message,"chatbot",client)
    m="Welcome "+clientinfo[client][0]+"\nYou can enter a message and click enter and\nif you want to exit the app, please enter QUIT"
    client.send(m.encode("ASCII"))
    while 1:
        received=client.recv(1024)
        received=received.decode("ASCII")
        print(received+" by "+clientinfo[client][0])
        if not received=="QUIT":
            broadcast(received,clientinfo[client][0],client)
        else:
            print(clientinfo[client][0]+" has quit the app")
            if len(groupinfo[clientinfo[client][1]][1])==1:
                 groupinfo.pop(clientinfo[client][1])
                 print(groupinfo)
                 m="Bye! Hope you come back soon..."
                 m=m.encode("ASCII")
                 client.send(m)
                 del clientinfo[client]
                 client.close()
                 break
                 
            m="Bye! Hope you come back soon..."
            m=m.encode("ASCII")
            client.send(m)
            name=clientinfo[client][0]
            groupn=clientinfo[client][1]
            groupinfo[groupn][1].remove(client)
            del clientinfo[client]
            broadcast(name+" has left the room","chatBot","",groupn)
            client.close()
            break
        
def broadcast(message,name,client="",group=""):
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

Host=""
port=8080
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
    
            
        
    
    
