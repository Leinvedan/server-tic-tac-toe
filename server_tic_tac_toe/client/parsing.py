import json

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
