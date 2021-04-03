from sys import stdin, stdout
import socket
import select


try:
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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
#can probably globalize the parts above

#The key diff for the client side
server.connect((IP_address, Port))

while True: 
    #Standard input:
    #It internally calls the input() method. It, also, automatically adds ‘\n’ after each sentence.
    
    sockets_list = [stdin, server]

    #Function to see if the message comes from the server or the user:
    read_sockets, write_socket, error_socket = select.select(sockets_list, [] ,[])

    for inputs in read_sockets:
        if inputs == server:
            print(inputs.recv(2048))
        else: 
            message = stdin.readline()
            server.send(bytes(message, "utf-8")
            stdout.write("<You>")
            stdout.write(message)
            stdout.flush()
            #do not forget about flushing

server.close()

