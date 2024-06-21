"""
Aplicações Distribuídas - Projeto 3 - net_client.py
Grupo: 01
Números de aluno: 60282
"""

import socket as s, pickle, struct, ssl
from sock_utils import *

class Client:
    """
    Represents a TCP client.
    """
        
    def __init__(self: object, host: str, port: int) -> None:
        """
        Initializes a Client object.

        Requires:
        host (str): The host IP address of the server.
        port (int): The port number of the server.
        Ensures:
        Initializing a Client object with the given attributes.
        """
        self._host = host
        self._port = port
        context = ssl.SSLContext(protocol=ssl.PROTOCOL_TLS_CLIENT) 
        context.verify_mode = ssl.CERT_REQUIRED
        context.check_hostname = True 
        context.load_verify_locations(cafile='root.pem') 
        context.load_cert_chain(certfile='cli.crt', keyfile='cli.key')
        self._sock = context.wrap_socket(create_tcp_client_socket(), server_hostname=host)
     
    # Getters and Setters
        
    @property
    def sock(self: object) -> s.socket:
        """
        Ensures:
        Returning this Client's socket.
        """
        return self._sock
    
    @property
    def host(self: object) -> str:
        """
        Ensures:
        Returning this Client's host.
        """
        return self._host
    
    @property
    def port(self: object) -> int:
        """
        Ensures:
        Returning this Client's port.
        """
        return self._port
    
    @sock.setter
    def sock(self: object, sock: s.socket) -> None:
        """
        Sets this Client's socket to a new value.

        Requires:
        sock (s.socket): The new Client socket.
        Ensures:
        Setting this Client's socket equal to the new given sock.
        """
        self._sock = sock
    
    @host.setter
    def host(self: object, host: str) -> None:
        """
        Sets this Client's host to a new value.

        Requires:
        host (str): The new Client's host
        Ensures:
        Setting this Client's host equal to the new given host.
        """
        self._host = host

    @port.setter
    def port(self: object, port: int) -> None:
        """
        Sets this Client's port to a new value.

        Requires:
        port (int): The new Client's port
        Ensures:
        Setting this Client's port equal to the new given port.
        """
        self._port = port

    # Methods
        
    def connect(self: object) -> None:
        """
        Ensures:
        Connecting to a server with this Client's host and port.
        """
        self.sock.connect((self.host, self.port))

    def receive_all(self: object) -> list:
        """
        Ensures:
        Receiving serialized messages from the server, unpacking them,
        and returning the received messages as a list.
        """
        size_bytes = self.sock.recv(4)
        size = struct.unpack('i', size_bytes)[0]

        msg_bytes = self.sock.recv(size)
        msg = pickle.loads(msg_bytes)

        return msg
    
    def send(self: object, msg: str) -> None:
        """
        Sends a message to the server.

        Requires:
        msg (str): The message to send.
        Ensures:
        Sending the serialized message to the server.
        """
        msg_bytes = pickle.dumps(msg, -1)
        size_bytes = struct.pack('i',len(msg_bytes))

        self.sock.sendall(size_bytes)
        self.sock.sendall(msg_bytes)

    def close(self: object) -> None:
        """
        Ensures:
        Closing this Client's socket.
        """
        self.sock.close()
            
    def __del__(self: object) -> None: 
        """
        Ensures:
        Closing this Client's socket when this Client is about to be destructed.
        """
        self.close()
