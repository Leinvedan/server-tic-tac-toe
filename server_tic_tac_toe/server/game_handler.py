from threading import Thread
import json
from server_tic_tac_toe.utils.logger_builder import create_logger


class GameHandler(Thread):
    def __init__(self, connection_1, connection_2, daemon=True):
        Thread.__init__(self, daemon=daemon)
        self.logger = create_logger(name=f'GAME', color='BLUE')
        self.player_1 = connection_1
        self.player_2 = connection_2

    def run(self):
        self.logger.info((
            f'Game starting: {self.player_1.name} '
            f'VS {self.player_2.name}'
        ))
        board = [['-', '-', '-'],
                 ['-', '-', '-'],
                 ['-', '-', '-']]
        isPlayer1Turn = True
        self.broadcast_board(board, isPlayer1Turn)

        while(True):
            try:
                if not self.both_players_connected():
                    self.logger.info('A player has left the game...')
                    # Return remaining player to the waiting list
                    break
                if isPlayer1Turn and self.player_1.command_available():
                    board = self.update_board(self.player_1, board, 'X')
                    isPlayer1Turn = False
                    self.broadcast_board(board, isPlayer1Turn)

                elif not isPlayer1Turn and self.player_2.command_available():
                    board = self.update_board(self.player_2, board, 'O')
                    isPlayer1Turn = True
                    self.broadcast_board(board, isPlayer1Turn)

            except Exception as e:
                self.logger.info(e)

    def update_board(self, connection, board, symbol):
        board = board.copy()
        command = connection.pop_command()
        board[command.line - 1][command.column - 1] = symbol
        for line in board:
            self.logger.info(line)
        return board

    def both_players_connected(self):
        return self.player_1.connected and self.player_2.connected

    def broadcast_board(self, board, isPlayer1Turn):
        message_player1 = json.dumps({
            'status': 'play' if isPlayer1Turn else 'wait',
            'board': board
        })
        message_player2 = json.dumps({
            'status': 'play' if not isPlayer1Turn else 'wait',
            'board': board
        })
        self.player_1.send_response(
            message_player1
        )
        self.player_2.send_response(
            message_player2
        )
