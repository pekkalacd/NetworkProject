import socket as sk
import random
import string
from socketmixin import SocketMixin, Socket
from dataclasses import dataclass

# server information
SERVER_HOST = "localhost"
SERVER_PORT = 5566

@dataclass
class Client(SocketMixin):

    host: str
    port: int
    socket = None

    def create_socket(self) -> Socket:
        sock: Socket = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
        sock.connect((self.host,self.port))
        return sock

        

def send_message(client_socket, msg: str):
    message = msg.encode("utf-8")
    msg_len = len(message)
    send_len = str(msg_len).encode("utf-8")
    send_len += b' ' * (1024 - len(send_len))
    client_socket.send(send_len)
    client_socket.send(message)

def unique_id() -> str:
    pool = string.ascii_letters + string.digits
    client_id: str = ''.join(random.choices(pool,k=7))
    return client_id


    


while True:

    with Client(SERVER_HOST,SERVER_PORT) as client_socket:

        client_id: str = unique_id()

        while (equation := input().lower()) != "exit":

            message = f"{client_id},{equation}"

            send_message(client_socket, message)

            solution = str(client_socket.recv(1024),'utf-8')

            print(f"server: {solution}")


        send_message(client_socket, f"{client_id},exit")
        break

        

    
        

    

    
