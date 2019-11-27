class BoardValidator():

    @staticmethod
    def update_board(board, command, is_player_1_turn):
        symbol = 'X' if is_player_1_turn else 'O'
        board = board.copy()
        board[command.line - 1][command.column - 1] = symbol
        return board

    @staticmethod
    def command_is_valid(board, command):
        is_inside_bounds = BoardValidator._command_is_inside_bounds(command)
        target_is_empty = False
        if is_inside_bounds:
            target_is_empty = board[command.line - 1][command.column - 1] == ''
        return target_is_empty and is_inside_bounds

    @staticmethod
    def _command_is_inside_bounds(command):
        line_valid = command.line <= 3 and command.line >= 1
        column_valid = command.column <= 3 and command.column >= 1
        return line_valid and column_valid

    @staticmethod
    def player_won(board):
        win_conditions = [
            BoardValidator._won_using_rows(board),
            BoardValidator._won_using_columns(board),
            BoardValidator._won_using_diagonals(board)
        ]
        for win in win_conditions:
            if win:
                return win
        return False

    @staticmethod
    def _won_using_rows(board):
        for row in board:
            if len(set(row)) == 1:
                return row[0]
        return False

    @staticmethod
    def _won_using_columns(board):
        board = board.copy()
        size = len(board)
        board = [[board[j][i] for j in range(size)] for i in range(size)]
        return BoardValidator._won_using_rows(board)

    @staticmethod
    def _won_using_diagonals(board):
        diagonal = [board[i][i] for i in range(len(board))]
        if len(set(diagonal)) == 1:
            return board[0][0]

        reversed_diagonal = [board[i][len(board)-i-1] for i in range(len(board))]
        if len(set(reversed_diagonal)) == 1:
            return board[0][len(board)-1]

        return False
