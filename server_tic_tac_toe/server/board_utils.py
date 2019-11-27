def update_board(board, command, is_player_1_turn):
    symbol = 'X' if is_player_1_turn else 'O'
    board = board.copy()
    board[command.line - 1][command.column - 1] = symbol
    return board


def command_is_valid(board, command):
    is_inside_bounds = _command_is_inside_bounds(command)
    target_is_empty = False
    if is_inside_bounds:
        target_is_empty = board[command.line - 1][command.column - 1] == ''
    return target_is_empty and is_inside_bounds


def _command_is_inside_bounds(command):
    line_valid = command.line <= 3 and command.line >= 1
    column_valid = command.column <= 3 and command.column >= 1
    return line_valid and column_valid


def _won_using_rows(board):
    for row in board:
        if len(set(row)) == 1:
            return row[0]
    return False


def _won_using_columns(board):
    board = board.copy()
    size = len(board)
    board = [[board[j][i] for j in range(size)] for i in range(size)]
    return _won_using_rows(board)


def _won_using_diagonals(board):
    if len(set([board[i][i] for i in range(len(board))])) == 1:
        return board[0][0]
    if len(set([board[i][len(board)-i-1] for i in range(len(board))])) == 1:
        return board[0][len(board)-1]
    return False


def player_won(board):
    win_conditions = [
        _won_using_rows(board),
        _won_using_columns(board),
        _won_using_diagonals(board)
    ]
    for win in win_conditions:
        if win:
            return win
    return False
