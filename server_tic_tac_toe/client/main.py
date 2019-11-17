import socket
import json

from server_tic_tac_toe.config import HOST, PORT
from server_tic_tac_toe.client.parsing import (
    read_coordinates_input,
    read_name_input,
    pretty_print_board
)

# testing client

tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp.connect((HOST, PORT))

print("Write your name:")

#  name confirmation
message_to_send = read_name_input()
tcp.sendall(message_to_send)

while message_to_send != "quit":
    response = tcp.recv(1024)
    response = response.decode('utf8')
    response = json.loads(response)
    pretty_print_board(response)

    if response['status'] == 'matched':
        print('Matched with other player!')

    elif response['status'] == 'play':
        # send play
        message_to_send = read_coordinates_input()
        tcp.sendall(message_to_send)

    elif response['status'] == 'waiting':
        print("Waiting match")

    elif response['status'] == 'error':
        print('[SERVER]:', response['message'])

        if response['error_type'] == 'INVALID_FORMAT':
            print('invalid format check the client`s code')
            exit()

        if response['error_type'] == 'INVALID_VALUES':
            print('invalid input, try again')
            message_to_send = read_coordinates_input()
            tcp.sendall(message_to_send)

        elif response['error_type'] == 'OPPONENT_LEFT':
            print('Waiting new game')
