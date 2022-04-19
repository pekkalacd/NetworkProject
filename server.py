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


############################################################################
# function:     printflush()
# parameters:   message: str
# return:       none
# description:  This function prints and flushes the server message to 
#               stdout.
############################################################################
def printflush(msg: str):
    print(msg)
    sys.stdout.flush()


############################################################################
# function:     format_time()
# parameters:   message: str
# return:       none
# description:  This function takes a time value and returns it formatted
#               as a string with hours, minutes, and seconds. 
############################################################################
def format_time(timeval: float) -> str:
    m,s = divmod(int(timeval),60)
    h,m = divmod(m,60)
    return f"{h:02d}:{m:02d}:{s:02d}"


############################################################################
# function:     client_handler()
# parameters:   socket: socket, ip_address: str
# return:       none
# description:  This function confirms session connection, listens for
#               client requests, processes the client request, and logs
#               server connection/processing events.
############################################################################
def client_handler(connection, addr):

    global CLIENTS


    # log client connection & send confirmation message
    lg.info(f"NEW_CONNECTION [ addr='{addr}' ]")
    printflush(f"[NEW CONNECTION] client at {addr} has connected")
    
    # receive initial message from client \r\n 
    msg_len = int(connection.recv(1024).decode("utf-8"))
    _,_ = connection.recv(msg_len).decode("utf-8").split(",")
    
    # send out confirmation msg - welcome
    confirmation_msg = "Ready to calculate equations consisting of real numbers\n" \
                         + "supporting addition (x + y), subtraction (x - y),\n" \
                         + "multiplication (x * y), division (x / y), modulus (x % y),\n" \
                         + "and exponents (x**y)"
    connection.send(confirmation_msg.encode('utf-8'))

    connected = True
    client_id = None
    # id_generated = False
    while connected:
        # process messages received
        if (msg_len := connection.recv(1024).decode('utf-8')):
            # parse message & requesting client
            msg_len = int(msg_len)
            client_id, equation = connection.recv(msg_len).decode('utf-8').split(',')

            # if not id_generated:
            #     lg.info(f"CLIENT_ID_GENERATED [ {addr} ] => {client_id}")
            #     printflush(f"[CLIENT-ID-GENERATED] for {addr} => {client_id}")
            #     id_generated = True

            # start client timer
            if client_id not in CLIENTS:
                CLIENTS[client_id] = {"start":time.time()}

            
            if equation == "exit":
                connection.send("Session terminated".encode('utf-8'))
                connected = False

            else:
                # log client request
                lg.info(f"CLIENT_REQUEST [ id={client_id} ] = {equation}")
                printflush(f"[CLIENT '{client_id}'] '{equation}'")

                try:
                    solution = str(eval(equation))
                    connection.send(solution.encode('utf-8'))
                except Exception:
                    lg.warning("BAD_REQUEST [ id={client_id} ] INVALID_EQ = {equation}")
                    connection.send("Bad Request:: Must be evaluable equation".encode("utf-8"))

    # terminate process & log duration
    CLIENTS[client_id].update({"end": time.time()})
    CLIENTS[client_id].update({"duration": format_time(CLIENTS[client_id]["end"] - CLIENTS[client_id]["start"])})
    lg.info(f"DISCONNECTION [ id={client_id}, addr={addr} ] - DURATION {CLIENTS[client_id]['duration']}")
    printflush(f"[DISCONNECTION] client {client_id} | {addr} :: duration {CLIENTS[client_id]['duration']}")
    connection.close()


############################################################################
# function:     start()
# parameters:   none
# return:       none
# description:  This function starts the server, listens for connections,
#               and logs connection events.
############################################################################
def start():

    with Server(host="localhost",port=5566) as welcome:
        lg.info(f"LISTENING [ Calc_Server ] - {welcome.getsockname()}")
        print(f"[LISTENING] Server is listening on {welcome.getsockname()}")
        while True:
            connection, addr = welcome.accept()
            thread = threading.Thread(target=client_handler, args=(connection, addr))
            thread.start()
            lg.info(f"ACTIVE_CONNECTIONS = {threading.active_count()-1}")
            print(f"[ACTIVE CONNECTIONS] {threading.active_count()-1}")


lg.basicConfig(handlers=[lg.FileHandler(filename='calc_server.log', encoding='utf-8')], 
               format='%(levelname)s: %(asctime)s - %(message)s', 
               level=lg.INFO)
# lg.info(f"LISTENING [ Server ] {}")
# print(f"[LISTENING] Server is listening on 'localhost'")
start()





            
    
    
