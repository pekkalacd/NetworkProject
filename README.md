# NetworkProject
Project for CS 4390


### usage 
open up two or more terminals, with one designated for the server, and the others as clients. 

for the server terminal `$ python server.py`

for the client terminals `$ python client.py`

type equations into the client terminals and observe the changes in both client and server terminals.<br>

### general idea
The `client.py` and `server.py` files both inherit from the `SocketMixin` class which provides a contextmanager,
allowing for automatic opening and closing of sockets. On the server side, since multiple clients are to connect,
threads are assigned per client connection and a `client_handler` function is targeted, which reads the message from the client, <br>
updates the server-side logs, and performs the calculation that is requested if possible. If the data sent from the client is not evaluable<br>
as an equation, an error message is sent back to the client, but the connection still persists.<br>

Only when the client enters **exit** will the client disconnect from the server. At which point, the duration for how long that client <br>
was connected is outputted to the console on the server side. The server continues to listen for any other clients.<br>
