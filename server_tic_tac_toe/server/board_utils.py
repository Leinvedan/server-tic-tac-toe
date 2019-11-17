def update_board(board, command, is_player_1_turn):
    symbol = 'X' if is_player_1_turn else 'O'
    board = board.copy()
    board[command.line - 1][command.column - 1] = symbol
    return board


def command_is_valid(board, command):
    is_inside_bounds = command_is_inside_bounds(command)
    target_is_empty = False
    if is_inside_bounds:
        target_is_empty = board[command.line - 1][command.column - 1] == '-'
    return target_is_empty and is_inside_bounds


def command_is_inside_bounds(command):
    line_valid = command.line <= 3 and command.line >= 1
    column_valid = command.column <= 3 and command.column >= 1
    return line_valid and column_valid
