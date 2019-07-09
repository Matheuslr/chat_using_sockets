"""
what client do:

1 - when the client make the connection with the server, client tells the server what the username he haves 

2 - from that point, make a infinity loop that if a client have adm on the name, sent to the server and
receive all messages that other users sent. A normal client only receive messages.

"""

import socket
import select
import errno
import sys


HEADER_LENGTH = 10
IP = "127.0.0.1"
PORT = 1234

my_username = input("Username: ")
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP, PORT)) # connect client to the server
client_socket.setblocking(False) #receive functionality won't be blocking

username = my_username.encode("utf-8") # encode the username
username_header = f"{len(username):<{HEADER_LENGTH}}".encode("utf-8") 
client_socket.send(username_header + username) # send the username

while True:
    if 'adm' in my_username:   
        message = input(f"{my_username} > ")
    else:
        message= ""
    if message:
        message = message.encode("utf-8") # encode the message
        message_header = f"{len(message) :<{HEADER_LENGTH}}".encode("utf-8")
        client_socket.send(message_header + message) # send the message
    try:
        while True: #recive messages
            username_header = client_socket.recv(HEADER_LENGTH)
            if not len(username_header): # if client get no message
                print("Connection closed by the server")
                sys.exit() # close program

            username_length = int(username_header.decode("utf-8").strip())
            username = client_socket.recv(username_length).decode("utf-8")# recive the user message length

            message_header = client_socket.recv(HEADER_LENGTH)
            message_length = int(message_header.decode("utf-8").strip())
            message = client_socket.recv(message_length).decode("utf-8")

            print(f"{username} > {message}")

    except IOError as e:
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print('Reading error', str(e))  
            sys.exit()
        continue

    # except Exception as e:
    #     print("General error", str(e))
    #     sys.exit()