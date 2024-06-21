"""
Aplicações Distribuídas - Projeto 3 - kuko_skel.py
Grupo: 01
Números de aluno: 60282
"""

import pickle, struct, socket as s
from net_server import *
from sock_utils import receive_all

class KukoSkeleton:
    """
    Represents a set of methods to connect to a server.
    """

    def __init__(self: object, sock: s.socket) -> None:
        """
        Initializes a KukoSkeleton instance.

        Requires:
        sock (s.socket): a socket object.
        host (str): The host address of the server.
        port (int): The port number of the server.
        Ensures:
        Initialiazing a KukoSkeleton object with the given attributes.
        """
        self._sock = sock

    # Getters and Setters

    @property
    def sock(self: object) -> s.socket:
        """
        Ensures:
        Returning the socket initialized in this KukoSkeleton.
        """
        return self._sock

    @sock.setter
    def sock(self: object, sock: s.socket) -> None:
        """
        Sets the socket initialized in this KukoSkeleton to a new value.

        Requires:
        sock (s.socket): a socket object.
        Ensures:
        Setting the socket initialized in this KukoSkeleton to a new socket.
        """
        self._sock = sock

    # Methods

    def requests_list(self: object) -> list[str]:
        """
        Ensures:
        Decoding the bytes sent to the socket in this KukoSkeleton by a client and
        returning a list of strings with the decoded data.
        """
        size_bytes = receive_all(self.sock)
        if not size_bytes:
            return None
        
        # Unpack the size bytes to get the size of the message
        msg_size = struct.unpack('i', size_bytes)[0]
        
        # Receive the serialized message
        msg_bytes = b''
        while len(msg_bytes) < msg_size:
            chunk =  self.sock.recv(min(msg_size - len(msg_bytes), 4096))
            if not chunk:
                return None
            msg_bytes += chunk
        
        # Deserialize the message
        requests_list = pickle.loads(msg_bytes)

        return requests_list
    
    def send_all(self: object, data: list[str]) -> None:
        """
        Sends a serialized list of strings from the socket in this KukoSkeleton.

        Requires:
        data (list[str]): A list of strings to be serialized and sent.
        Ensures:
        Sending the serialized list to a client connected to the 
        socket in this KukoSkeleton.
        """
        # Serialize the data
        serialized_data = pickle.dumps(data)
        
        # Get the size of the serialized data
        data_size = len(serialized_data)
        size_bytes = struct.pack('i', data_size)
        
        # Send the size of the data
        self.sock.sendall(size_bytes)
        
        # Send the serialized data
        sent_bytes = 0
        while sent_bytes < data_size:
            remaining_bytes = data_size - sent_bytes
            chunk = serialized_data[sent_bytes:sent_bytes + remaining_bytes]
            sent_bytes += self.sock.send(chunk)

    def close_socket(self: object) -> None:
        """
        Ensures:
        Closing the socket in this KukoSkeleton.
        """
        self.sock.close()