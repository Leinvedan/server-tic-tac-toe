from threading import Thread
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
        self.player_1.send_response({'status': 'matched'})
        self.player_2.send_response({'status': 'matched'})
        self.broadcast_board(board, isPlayer1Turn)

        while(self.both_players_connected()):
            try:
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
        self.logger.info((
            f'{self.player_1.name} VS {self.player_2.name} game has ended'
            '... Closing session'
        ))

    def update_board(self, connection, board, symbol):
        board = board.copy()
        command = connection.pop_command()
        board[command.line - 1][command.column - 1] = symbol
        for line in board:
            self.logger.info(line)
        return board

    def both_players_connected(self):
        if self.player_1.connected and self.player_2.connected:
            return True
        else:
            ERROR_MESSAGE = {
                'status': 'error',
                'message': (
                    'Your opponent has left the game,'
                    'returning to waiting room'
                )
            }

            for player in [self.player_1, self.player_2]:
                if not player.connected:
                    self.logger.info(f'{player.name} has left the game...')
                player.set_waiting_match(True)
                player.send_response(ERROR_MESSAGE)

        return False

    def broadcast_board(self, board, isPlayer1Turn):
        message = {
            'status': None,
            'board': board
        }

        message['status'] = 'play' if isPlayer1Turn else 'wait'
        self.player_1.send_response(message)

        message['status'] = 'play' if not isPlayer1Turn else 'wait'
        self.player_2.send_response(message)
