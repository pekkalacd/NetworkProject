import socket as sk
import sys
import os
# import random
import string
import ipaddress as ip
from socketmixin import SocketMixin, Socket
from dataclasses import dataclass

# # server information
# SERVER_HOST = "localhost"
# SERVER_PORT = 5566

@dataclass
class Client(SocketMixin):

    host: str
    port: int
    socket = None

    def create_socket(self) -> Socket:
        sock: Socket = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
        sock.connect((self.host,self.port))
        return sock
        
############################################################################
# function:     send_message()
# parameters:   socket: socket, server_request: str
# return:       none
# description:  This function takes the user input and associated socket
#               encodes the message, and sends the request to the server
############################################################################
def send_message(client_socket, msg: str):
    message = msg.encode("utf-8")
    msg_len = len(message)
    send_len = str(msg_len).encode("utf-8")
    send_len += b' ' * (1024 - len(send_len))
    client_socket.send(send_len)
    client_socket.send(message)


############################################################################
# function:     unique_id()
# parameters:   server_ip_address: str, socket: socket
# return:       id: str
# description:  This function takes the server IP address and if the
#               server is running on 'localhost', the client id is
#               based on the local process id, else the client id is
#               based on the client's ip address as int. The base
#               value is used with the pooled characters to build a
#               unique client id that contains characters a-z or A-Z,
#               and/or digits 0-9. 
############################################################################
def unique_id(SERVER_HOST, client_socket) -> str:
    # possible id characters
    pool = string.ascii_letters + string.digits
    # determine if ip or pid-based id
    if SERVER_HOST == 'localhost':
        int_id = os.getpid()
    else:
        int_id = int(ip.ip_address(client_socket.gethostname()))
    
    # build id using pooled characters
    client_id = ''
    while int_id:
        r = int_id % len(pool)
        int_id = int(int_id / len(pool))
        client_id += pool[r]

    return client_id


############################################################################
# function:     run_client()
# parameters:   server_ip_address, server_port_number
# return:       none
# description:  This function sets the client id, gets user input as a
#               server request, and calls the function to send the user
#               request. This function terminates when the user enters
#               the 'exit' request.
############################################################################
def run_client(SERVER_HOST, SERVER_PORT):
    while True:

        with Client(SERVER_HOST,SERVER_PORT) as client_socket:
            client_id: str = unique_id(SERVER_HOST, client_socket)

            while (equation := input().lower()) != "exit":
                # parse user input
                message = f"{client_id},{equation}"
                send_message(client_socket, message)
                solution = str(client_socket.recv(1024),'utf-8')
                print(f"Calc-Server: {solution}")

            # send termination request
            send_message(client_socket, f"{client_id},exit")
            break


if __name__ == '__main__':
    if len(sys.argv[1:]) != 2:
        # server information
        SERVER_HOST = "localhost"
        SERVER_PORT = 5566
    else:
        # server information
        SERVER_HOST = sys.argv[1]
        SERVER_PORT = int(sys.argv[2])
    
    run_client(SERVER_HOST, SERVER_PORT)
