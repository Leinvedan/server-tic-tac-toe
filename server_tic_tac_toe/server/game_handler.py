from threading import Thread
import json
from server_tic_tac_toe.utils.logger_builder import create_logger


class GameHandler(Thread):
    def __init__(self, connection_1, connection_2, daemon=True):
        Thread.__init__(self, daemon=daemon)
        self.logger = create_logger(name=f'GAME', color='BLUE')
        self.connection_1 = connection_1
        self.connection_2 = connection_2

    def run(self):
        self.logger.info((
            f'Game starting: {self.connection_1.name}'
            f'VS {self.connection_2.name}'
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
                    break
                if isPlayer1Turn and self.connection_1.get_command():
                    command = self.connection_1.get_command()
                    board[command.line][command.column] = 'X'
                    isPlayer1Turn = False
                    self.logger.info(board)
                    self.broadcast_board(board, isPlayer1Turn)

                elif not isPlayer1Turn and self.connection_2.get_command():
                    command = self.connection_2.get_command()
                    board[command.line][command.column] = 'O'
                    isPlayer1Turn = True
                    self.logger.info(board)
                    self.broadcast_board(board, isPlayer1Turn)

            except Exception as e:
                self.logger.info(e)

    def both_players_connected(self):
        return self.connection_1.connected and self.connection_2.connected

    def broadcast_board(self, board, isPlayer1Turn):
        message_player1 = json.dumps({
            'status': 'play' if isPlayer1Turn else 'wait',
            'board': board
        })
        message_player2 = json.dumps({
            'status': 'play' if not isPlayer1Turn else 'wait',
            'board': board
        })
        self.connection_1.send_response(
            message_player1,
            clear_command=True
        )
        self.connection_2.send_response(
            message_player2,
            clear_command=True
        )
