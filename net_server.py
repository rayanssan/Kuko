"""
Aplicações Distribuídas - Projeto 3 - net_server.py
Grupo: 01
Números de aluno: 60282
"""

import socket as s, ssl
from sock_utils import *

class Server:
    """
    Represents a TCP server.
    """
        
    def __init__(self: object, host: str, port: int) -> None:
        """
        Initializes a Server object.

        Requires:
        host (str): The host IP address to bind this Server socket to.
        port (int): The port number to bind this Server's socket to.
        Ensures:
        Initializing a Server object with the given attributes.
        """
        context = ssl.SSLContext(protocol=ssl.PROTOCOL_TLS_SERVER) 
        context.verify_mode = ssl.CERT_REQUIRED 
        context.load_verify_locations(cafile='root.pem') 
        context.load_cert_chain(certfile='serv.crt', keyfile='serv.key')
        self._sock = context.wrap_socket(create_tcp_server_socket(host, port), server_side=True)
    
    # Getters and Setters
        
    @property
    def sock(self: object):
        """
        Ensures:
        Returning this Server's socket.
        """
        return self._sock
    
    @sock.setter
    def sock(self: object, sock: s.socket) -> None:
        """
        Sets this Server's socket to a new value.

        Requires:
        sock (s.socket): The new Server socket.
        Ensures:
        Setting this Server's socket equal to the new given sock.
        """
        self._sock = sock

    # Methods 
        
    def accept(self: object) -> tuple:
        """
        Ensures:
        Accepting a connection on this Server's socket
        and returning a tuple containing the new socket object and the address of the client.
        """
        return self.sock.accept()

    def listen(self: object) -> None:
        """
        Ensures:
        Listening for connections on this Server's socket.
        """
        self.sock.listen()

    def close(self: object) -> None:
        """
        Ensures:
        Closing this server's socket.
        """
        self.sock.close()

    def __del__(self: object) -> None:
        """
        Ensures:
        Closing this Server's socket when this Server is about to be destructed.
        """
        if hasattr(self, '_sock') and self._sock is not None:
            self.close()



