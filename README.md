# NetworkProject
Project for CS 4390

### preliminary requirements and dependencies
Please ensure you are using Python version 3.8 or above.
Ensure you have dataclasses module (pip install dataclasses)


### usage 
In the case that the server process and each client process are executed on the same local host:
    open up two or more terminals, with one designated for the server and the others as clients
    for the server terminal: `$ python server.py`
    for each client terminal: `$ python client.py`

In the case that the server process is executed on a host at a different IP address:
    open up a terminal on each host to run the server process and each client process
    for the server terminal: `$ python server.py [<host_ip_address> <host_port_number>`
    for each client terminal: `$ python client.py <server_ip_address> <server_port_number>`

type equations into the client terminals and observe the changes in both client and server consoles

type **exit** in each active client terminal to terminate client-server sessions<br>

### explanation
The `client.py` and `server.py` files both inherit from the `SocketMixin` class which provides a contextmanager, allowing for automatic opening and closing of sockets. On the server side, since multiple clients are to connect, threads are assigned per client connection and a `client_handler` function is targeted, which reads the message from the client, updates the server-side logs, and performs the calculation that is requested if possible. If the data sent from the client is not evaluable, an error message is sent back to the client, the invalid request is logged as a warning-level event, and the connection still persists.<br>

When the client enters **exit** the server processes the termination request and closes the connection. At which point, the duration of the client is logged as an information-level event and the count of active connections is updated.<br>

The server.py file does more than the client.py file. The client.py is a simple client, continually waiting for user input from the console to
send as a message to the server. Whereas the server.py is a threaded concurrent process. In addition to the threading, the client_handler function
handles three server features: 1) processing client-side messages, evaluating equations and returning the solution to the appropriate client,
2) maintaining record of when each client connected and when they disconnect, wherein the duration of the session is logged, and 3) event logging
for when a new client has connected, when they send en equation resolution request, and when they send a session termination request.<br>

Both the Client and Server classes make sockets based on IPv4. The name `sk` is an alias used for the module `socket` imported in each file, and `sk.socket` is the class that's responsible for creating the sockets themselves. `sk.AF_INET` along with `sk.SOCK_STREAM` are used for both, which is TCP/IPv4. In the Client class, the `create_socket` method is invoked to create the socket and connect it to the server host and port number in one step.

In the Server class, the `create_socket` method creates a reusable socket via `sk.SOL_SOCKET` and `sk.SO_REUSEADDR`, binds it to provided host and port number, and then listens for up to 10 undiscovered client connections before refusing additional ones (`listen(10)`).<br>

The SocketMixin class contains three things: an abstract method for `create_socket` since its subclasses both implemented their own version, an `__enter__` method which invokes the create_socket method from a subclass then returns the socket upon entry to a block within a context manager scope
marked by `with`, and an `__exit__` method which determines how exiting that context manager is handled, in this case, the socket that is created for the client or server is closed, and if an error occurs in the process of doing so, a traceback is printed.<br>

### capabilities
This program is capable of connecting multiple clients concurrently to a single server. The messages the server can evaluate are bound to numerical equations with builtin python operators. It can perform evaluations on integers, floats, scientific notation expressions or any combination of the previous. This program ensure that equations are resolvable, provides appropriate responses in the case of invalid or valid server requests, and provides record of information-level and above events, available in the server side log. 
