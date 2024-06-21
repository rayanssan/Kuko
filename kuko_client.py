"""
Aplicações Distribuídas - Projeto 3 - kuko_client.py
Grupo: 01
Números de aluno: 60282
"""

import sys, json
from net_client import *
from kazoo.client import KazooClient

def main(id_participant: int, host: str, port: int) -> None:
    """
    Creates a Kuko client.

    Requires:
    id_participant (int): The unique identifier of the participant.
    host (str): The host address of the server.
    port (int): The port number of the server.
    Ensures:
    Creating a Kuko client with the specified host and port.
    """
    try:
        client = Client(host, port)
        print(f"ligado a {host}:{port}")
        client.connect()
        communication = True

        zookeeper = KazooClient()
        zookeeper.start() 
          
        notify = False
        @zookeeper.DataWatch('/question')
        def watch_questions(data: object, stat: object) -> None:
            """
            Watches for changes on the /question znode and notifies this client if 
            a change happens.
            
            Requires:
            data (object): The data associated with the watched node.
            stat (object): The stat information associated with the watched node.
            Ensures:
            Watching the /question znode and notifying this client if any changes happen.
            """
            nonlocal notify
            if notify:
                print('\n'+json.dumps({data.decode(): "NEW QUESTION"}))
            else:
                notify = True

        while (communication):
            try:
                message = input("comando > ")
                if not message:
                    message = ' '
                message = message.split(';')
                message.append(str(id_participant))
                client.send(message)
                print(f"SENT:{ {f'arg{message.index(x)}': x for x in message} }")
                answer = client.receive_all()
                if message[0] == "EXIT" or answer[0] == "EXIT":
                    print(f"RECV:{ {'response': answer[0]} }")
                    if answer == "EXIT":
                        print("A conexão com o servidor foi interrompida.")
                    communication = False
                else:
                    print(f"RECV:{answer}")
            except (ConnectionResetError, BrokenPipeError, struct.error, ssl.SSLEOFError):
                print(f"RECV:{ {'arg0': 'EXIT'} }")
                print("A conexão com o servidor foi interrompida.")
                communication = False
            except Exception as e:
                print(f"Ocorreu um erro: {e}")
                pass
    except KeyboardInterrupt:
        print(" - Cliente interrompido.")
        try:
            client.send(["EXIT"])
            print(f"SENT:{ {'arg0': 'EXIT', 'arg1': id_participant} }")
            answer = client.receive_all()
            print(f"RECV:{ {'response': answer[0]} }")
            exit()
        except Exception:
            pass
    finally:
        zookeeper.stop()
        del client

if __name__ == "__main__":
    id_participant = sys.argv[1]
    host = sys.argv[2]
    port = int(sys.argv[3])
    main(id_participant, host, port)