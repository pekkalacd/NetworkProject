import socket as sk
import traceback
from typing import TypeVar, Optional
from dataclasses import dataclass
from abc import abstractmethod

Socket = TypeVar('Socket',bound=sk.socket)

@dataclass
class SocketMixin:

    @abstractmethod
    def create_socket(self) -> Socket:
        """creates a socket for the given subclass (Client/Server)"""

    def __enter__(self):

        sock: Socket = self.create_socket()
        self.socket = sock
        return self.socket

    def __exit__(self, *exit_info):

        if exit_info[0]:
            traceback.print_exception(*exit_info)

        self.socket.close()
        

    
        

