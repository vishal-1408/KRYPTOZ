
from threading import Thread
import socket



def receive():
    i=1
    print('Function Started!!!!')
    while 1:
        try:
            m=client.recv(1024)
            m=m.decode("ASCII")
            print(m)
            if(m[0:3]=="Bye"):
                client.close()
                
        except OSError:
           print("Connection got disconnected")
           break


def send(event=None):
    m= message.get()
    message.set("")
    m=m.encode("ASCII")
    client.send(m)
    print(m)
    
        


    

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

def close():
    client.close()

client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#Host=input("Enter the host name: ")
#Port=int(input("Enter the port number: "))
#Host="34.227.91.249"
def client_initialize():
    Host="127.0.0.1"
    Port=8080
    client.connect((Host,Port))  
    rthread=Thread(target=receive)
    rthread.start()


    

