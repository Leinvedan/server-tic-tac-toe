import socket
import json

from server_tic_tac_toe.config import HOST, PORT
from server_tic_tac_toe.parsing import (
    read_coordinates_input,
    read_input,
    pretty_print_board
)

# testing client

try:
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp.connect((HOST, PORT))

    print("Write message:")

    #  name confirmation
    message_to_send = read_input()
    tcp.sendall(message_to_send)

    while message_to_send != "quit":
        response = tcp.recv(1024)
        response = response.decode('utf8')
        response = json.loads(response)
        pretty_print_board(response)

        if response['status'] == 'matched':
            print('Server: Matched with other player!')

        elif response['status'] == 'play':
            # send play
            message_to_send = read_coordinates_input()
            tcp.sendall(message_to_send)

        elif response['status'] == 'error':
            print('Error received:', response['message'])
            print('Waiting new game')

        elif response['status'] == 'waiting':
            print("server:", response['message'])


except KeyboardInterrupt:
    print("Exiting...")
finally:
    tcp.close()
