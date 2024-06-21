import socket as s, sys

def create_tcp_server_socket(address: str, port: int) -> s.socket:
    """
    Creates a TCP server socket.

    Requires:
    address (str): The IP address to bind the socket to.
    port (int): The port number to bind the socket to.
    Ensures:
    Returning the created TCP server socket.
    """
    try:
        sock = s.socket(s.AF_INET, s.SOCK_STREAM)
        sock.setsockopt(s.SOL_SOCKET, s.SO_REUSEADDR, 1)
        sock.bind((address, port))
        return sock
    except OSError:
        print("este endereço já está em utilização.")
        sys.exit()

def create_tcp_client_socket() -> s.socket:
    """
    Ensures:
    Creating a TCP client socket and returning it.
    """
    sock = s.socket(s.AF_INET, s.SOCK_STREAM)
    return sock

def receive_all(sock: s.socket) -> bytes:
    """
    Receives bytes from a socket.

    Requires:
    sock (s.socket): a socket object.
    Ensures:
    Receiving bytes sent to the given socket.
    """
    return sock.recv(4)

def notify_question_insert(self, zookeeper, question_id: int):
    """
    Notify ZooKeeper about successful question insertion.

    Requires:
    question_id (int): ID of the inserted question.
    """
    # Update the znode value to notify clients
    zookeeper.set("/question_insert", str(question_id).encode())
