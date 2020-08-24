
from threading import Thread
import socket



def accept():
    i=0
    while 1:                                                             #threads are just created for making blocks of code execute parallely! like accepting the connections and handling clients all these work in parallel
        client_socket,client_addr = server_socket.accept()
        print("A client has been connected to the server")
        address[client_socket]=client_addr
        client_socket.sendall("Please enter your name and click enter".encode("ASCII"))
        message = client_socket.recv(1024)
        message=message.decode('ASCII')
        client_name[client_socket]=message
        Thread(target=handling_the_client,args=(client_socket,)).start()
        print(len(client_name))
        i+=1
        

def handling_the_client(client):
    message=client_name[client]+" has joined the chat app!"
    broadcast(message,"chatbot",client)
    m="Welcome "+client_name[client]+"\nYou can enter a message and click enter and\nif you want to exit the app, please enter QUIT"
    client.send(m.encode("ASCII"))
    while 1:
        received=client.recv(1024)
        received=received.decode("ASCII")
        print(received+" by "+client_name[client])
        if not received=="QUIT":
            broadcast(received,client_name[client])
        else:
            print(client_name[client]+" has quit the app")
            m="Bye! Hope you come back soon..."
            m=m.encode("ASCII")
            client.send(m)
            name=client_name[client]
            del client_name[client]
            del address[client]
            broadcast(name+" has left the room","ChatBot")
            client.close()
            break
        
def broadcast(message,name="",client=""):
    if client=="":
        for x in client_name:
            m=name+" : "+message
            m=m.encode("ASCII")
            x.send(m)
    else:
        for x in client_name:
            if not x==client:
                m=name+" : "+message
                m=m.encode("ASCII")
                x.send(m)

address = {}
client_name = {}
Host="127.0.0.1"
port=3000
server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

server_socket.bind((Host,port))


if __name__ == "__main__":
    server_socket.listen(10)
    print("Socket is listening for sockets!!")
    main_thread=Thread(target=accept)
    main_thread.start() #starts the thread
    main_thread.join() #blocks the code here till the main_threads execution doesn't end!
    server_socket.close()
    
            
        
    
    
