import json


def read_coordinates_input():
    command = None
    while True:
        try:
            command = input(">").split(' ')
            command = {'line': command[0], 'column': command[1]}
            command = json.dumps(command)
            break
        except Exception:
            # make a better validation
            print('Invalid values, try again')
    return bytes(command, encoding='utf8')


def read_named_input(field_name):
    value = input(">")
    json_obj = json.dumps({field_name: value})
    return bytes(json_obj, encoding='utf8'), value


def pretty_print_board(response):
    if 'board' in response:
        for line in response['board']:
            print(line)
        print()
