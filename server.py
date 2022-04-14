import socket as sk
import threading
import time
import sys
import logging as lg
from dataclasses import dataclass
from socketmixin import SocketMixin, Socket


CLIENTS = dict()

@dataclass
class Server(SocketMixin):

    host: str
    port: int
    socket = None

    def create_socket(self) -> Socket:
        sock: Socket = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
        sock.setsockopt(sk.SOL_SOCKET, sk.SO_REUSEADDR,1)
        sock.bind((self.host,self.port))
        sock.listen(10)
        return sock


def printflush(msg: str):
    print(msg)
    sys.stdout.flush()

def format_time(timeval: float) -> str:
    m,s = divmod(int(timeval),60)
    h,m = divmod(m,60)
    return f"{h:02d}:{m:02d}:{s:02d}"


def client_handler(connection, addr):

    global CLIENTS

    lg.info(f"[NEW CONNECTION] client at {addr} has connected")
    printflush(f"[NEW CONNECTION] client at {addr} has connected")

    connected = True
    client_id = None
    id_generated = False
    while connected:

        if (msg_len := connection.recv(1024).decode('utf-8')):

            msg_len = int(msg_len)
            client_id, equation = connection.recv(msg_len).decode('utf-8').split(',')

            if not id_generated:
                lg.info(f"[CLIENT-ID-GENERATED] for {addr} => {client_id}")
                printflush(f"[CLIENT-ID-GENERATED] for {addr} => {client_id}")
                id_generated = True

            if client_id not in CLIENTS:
                CLIENTS[client_id] = {"start":time.time()}
            
            if equation == "exit":
                connected = False

            lg.info(f"[CLIENT {client_id}] {equation}")
            printflush(f"[CLIENT {client_id}] {equation}")

            try:
                solution = str(eval(equation))
                connection.send(solution.encode('utf-8'))
            except Exception:
                lg.warning("Bad Request:: Must be evaluable equation".encode("utf-8"))
                connection.send("Bad Request:: Must be evaluable equation".encode("utf-8"))

    CLIENTS[client_id].update({"end": time.time()})
    CLIENTS[client_id].update({"duration": format_time(CLIENTS[client_id]["end"] - CLIENTS[client_id]["start"])})
    lg.info(f"[DISCONNECTION] client {client_id} | {addr} :: duration {CLIENTS[client_id]['duration']}")
    printflush(f"[DISCONNECTION] client {client_id} | {addr} :: duration {CLIENTS[client_id]['duration']}")
    connection.close()




def start():

    with Server(host="localhost",port=5566) as welcome:
        while True:
            connection, addr = welcome.accept()
            thread = threading.Thread(target=client_handler, args=(connection, addr))
            thread.start()
            lg.info(f"[ACTIVE CONNECTIONS] {threading.active_count()-1}")
            print(f"[ACTIVE CONNECTIONS] {threading.active_count()-1}")


lg.basicConfig(filename='calc_server.log', encoding='utf-8', level=lg.INFO)
lg.info(f"[LISTENING] Server is listening on 'localhost'")
print(f"[LISTENING] Server is listening on 'localhost'")
start()





            
    
    
