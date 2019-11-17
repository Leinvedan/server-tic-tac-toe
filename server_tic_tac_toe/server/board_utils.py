def update_board(connection, board, symbol):
    board = board.copy()
    command = connection.pop_command()
    board[command.line - 1][command.column - 1] = symbol
    return board


def command_is_valid(board, command):
    return board[command.line][command.column] == '-'


def command_is_inside_bounds(command):
    line_valid = command.line <= 3 and command.line >= 1
    column_valid = command.column <= 3 and command.column >= 1
    return line_valid and column_valid
