import sys, select
from net_server import *
from kuko_data import *
from kuko_skel import *
from kuko_stub import *
from kazoo.client import KazooClient

def main(host: str, port: int) -> None:
    """
    Creates a Kuko server.

    Requires:
    host (str): The host address of the server.
    port (int): The port number of the server.
    Ensures:
    Creating a Kuko server with the specified host and port.
    """
    try:
        server = Server(host, port)
        if server.sock != None:
            server.listen()
            print('À escuta')
            
            sockets_list = [server.sock]
            clients = {} 

            kuko = Kuko()
            zookeeper = KazooClient()
            zookeeper.start()
        
            while (sockets_list):
                try:
                    readable, _, _ = select.select(sockets_list, [], [])
                    for sock in readable:
                        skel = KukoSkeleton(sock)
                        if sock == server.sock:
                            client_sock, (client_host, client_port) = server.accept()
                            print(f"ligado a {client_host}:{client_port}")
                            sockets_list.append(client_sock)
                            clients[client_sock] = client_host
                        else:
                            requests_list = skel.requests_list()
                            if requests_list:
                                stub = KukoStub(requests_list, skel, kuko)
                                print(f"RECV:{ {f'arg{requests_list.index(x)}': x for x in requests_list} }")
                                if requests_list[0] == "EXIT":
                                    # EXIT
                                    server_ans = ["True"]
                                    skel.send_all(server_ans)
                                    print(f"SENT:{json.dumps({'response': server_ans[0]})}")
                                    clients.pop(sock)
                                    sockets_list.remove(sock)
                                    skel.close_socket()
                                else:
                                    all_numeric = all(x.isdigit() for x in requests_list)
                                    if requests_list[0] == '60' and all_numeric and len(requests_list) == 3:
                                        # REG (60)
                                        stub.reg()
                                    elif requests_list[0] == '70' and all_numeric and len(requests_list) == 3:
                                        # GET (70)
                                        stub.get()
                                    elif requests_list[0] == '80' and all_numeric and len(requests_list) == 4:
                                        # ANS (80)
                                        stub.ans()
                                    elif requests_list[0] == "90" and all_numeric and len(requests_list) == 3:
                                        # REL (90)
                                        stub.rel()
                                    elif requests_list[0] == "10" and len(requests_list) > 3 and requests_list[-2].isdigit():
                                        # QUESTION (10)
                                        stub.question(zookeeper)
                                    elif requests_list[0] == "20" and all_numeric and len(requests_list) > 2:
                                        # QSET (20)
                                        stub.qset()
                                    elif requests_list[0] == "30" and all_numeric and len(requests_list) > 3:
                                        # QUIZ (30)
                                        stub.quiz()
                                    elif requests_list[0] == "40" and all_numeric and len(requests_list) == 3:
                                        # LAUNCH (40)
                                        stub.launch()
                                    elif requests_list[0] == "50" and all_numeric and len(requests_list) == 3:
                                        # NEXT (50)
                                        stub.next()
                                    else:
                                        # Invalid command -> ERROR
                                        stub.error()
                            else:
                                # Client disconnected
                                # EXIT
                                print(f"RECV:{ {'arg0': 'EXIT'} }")
                                clients.pop(sock)
                                sockets_list.remove(sock)
                                skel.close_socket()
                except Exception as e:
                    print(f"Ocorreu um erro: {e}")
                    pass
    except KeyboardInterrupt:
        zookeeper.stop()
        print(" - Servidor interrompido.")
        exit()

if __name__ == "__main__":
    host = sys.argv[1]
    port = int(sys.argv[2])
    main(host, port)
