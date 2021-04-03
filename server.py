""" This is the server that will keep running
"""
import socket
import select 
import sys
import thread

#AF_INTET refers to the address ipv4. SOCK_STREAM is using the connection-oriented TCP protocol( Transmission Control Protocol)
#since the connection between client and server is needed before the data is sent
#TCP would accept data from a data stream, divide it into chuncks and add a TCP header creating a tCP segment
#then encapsulated into Internet Protocol datagram and given to the peers

try:
    server = socket.socket(socket.AF_INET), socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
    print ("Socket successfully created!")
except socket.error as err:
    print(f"Socket creattion failed with error {err}")
#Create connection or print the error 

#Now to limit users/client to 100:
if len(sys.argv) !=3:
    print ("Correct usage: script, IP address, portnumber")
    exit()

IP_address = str(sys.argv[1])

Port = int(sys.argv[2])

server.bind((IP_address, Port))

server.listen(100)

active_clients =[]

#Connecting and sending welcome message
def clientthread(conn, addr):
    conn.send("Welcome to this chatroom")

    #Prints the message and address of the user to the server terminal 
    while True:
        try:
            message = conn.recv(2048)
            if message:
                print("<" + addr[0]+ ">" + message)
                #Calls broadcast(line 57) function to the server
                message_to_send= "<" + addr[0]+ ">" + message
                broadcast(message_to_send, conn)

            else: 
                #if no message with the connection broken, remove the connection
                remove(conn)
        except:
            continue
 
#send the message to all the other clients than the sender
def broadcast(message, connection):
    for clients in active_clients:
        if clients != connection:
            try:
                client.send(message)
            except:
                clients.close()
                #remove is the client isn't connected Line 68
                remove(clients)

#this is remove function
def remove(connection):
    if connection in active_clients:
        active_clients.remove(connection)


while True:
    #Unpacking to declare the conn and addr from server.accept()
    conn, addr = server.accept() 
    #add the conn into the active_clients list
    active_clients.append(conn)
    #print the address of the user that just connected
    print(addr[0] + "connected")
    #Start the new thread for all that connects
    thread.start_new_thread(clientthread),(conn,addr))

conn.close()
server.close()




