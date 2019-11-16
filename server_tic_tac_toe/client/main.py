import socket
import json

from server_tic_tac_toe.config import HOST, PORT

# testing client


def read_coordinates_input():
    command = input(">").split(' ')
    command = {'line': command[0], 'column': command[1]}
    command = json.dumps(command)
    return bytes(command, encoding='utf8')


def read_input():
    command = input(">")
    return bytes(command, encoding='utf8')


def pretty_print_board(response):
    if 'board' in response:
        for line in response['board']:
            print(line)


try:
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    dest = (HOST, PORT)
    tcp.connect(dest)

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
