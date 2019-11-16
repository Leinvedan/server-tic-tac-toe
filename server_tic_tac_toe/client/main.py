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


try:
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    dest = (HOST, PORT)
    tcp.connect(dest)

    print("Write message:")

    #  name confirmation
    message_to_send = read_input()
    tcp.sendall(message_to_send)
    response = tcp.recv(1024)
    print("server:", response.decode('utf8'))

    while message_to_send != "quit":
        response = tcp.recv(1024)
        response = response.decode('utf8')
        response = json.loads(response)
        print("server:", response)
        print(response['status'])
        for line in response['board']:
            print(line)
        if (response['status'] == 'play'):
            # send play
            message_to_send = read_coordinates_input()
            tcp.sendall(message_to_send)

except KeyboardInterrupt:
    print("Exiting...")
finally:
    tcp.close()
