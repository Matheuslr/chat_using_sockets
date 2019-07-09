import socket
import select

HEADER_LENGTH = 10
IP = "127.0.0.1"
PORT = 1234

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)# IPV4, TCP
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # setting to not get the "address aready in use" message

server_socket.bind((IP, PORT))# binding ip/port

server_socket.listen() # server is listening now

sockets_list = [server_socket] 

clients = {}


def receive_message(client_socket):
    try:
        message_header = client_socket.recv(HEADER_LENGTH)#get the message header

        if not len(message_header): # check if message is sent
            return False
        
        message_length = int(message_header.decode("utf-8").strip())#convert the size of the message
        return {"header": message_header, "data": client_socket.recv(message_length)} #return the message content
        
    except: # if something broke the connection
        return False


while True: #maintain the connection server-client
    read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)#read list and sockets with error

    for notified_socket in read_sockets:
        if notified_socket == server_socket: #someone just connect, handle the connection
            client_socket, client_address = server_socket.accept() # accept the connection

            user = receive_message(client_socket) # get the user infos
            if user is False: #if someone disconnect
                continue

            sockets_list.append(client_socket)# add

            clients[client_socket] = user # add the new client to the client list

            print(f"Accepted new connection from {client_address[0]}:{client_address[1]} \
                username:{user['data'].decode('utf-8')}")

        else: # user already connected
            message = receive_message(notified_socket)#get user message

            if message is False: # message not sent
                print(f"Closed  connection from {clients[notified_socket]['data'].decode('utf*8')}")
                sockets_list.remove(notified_socket) #remove client from the socket list
                del clients[notified_socket] #remove client from the client dictionary
                continue # continue the while
            
            user = clients[notified_socket] # get the user info adn message in the clients dictionary
            
            print(f"Received message from {user['data'].decode('utf-8')}: {message['data'].decode('utf-8')} ")

            for client_socket in clients: #broadcast the message
                if client_socket != notified_socket: # checking if client_socket are not the user
                    client_socket.send(user['header'] + user['data'] 
                    + message['header'] + message['data']) #broadicastin the message
        
    for notified_socket in exception_sockets: #handling the sockets with error
        sockets_list.remove(notified_socket)
        del clients[notified_socket] #remove the sockets with some error 
