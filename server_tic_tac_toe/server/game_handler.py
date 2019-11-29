from threading import Thread
from server_tic_tac_toe.utils.logger_builder import create_logger
from server_tic_tac_toe.server.board_validator import BoardValidator


class GameHandler(Thread):
    def __init__(self, connection_1, connection_2, daemon=True):
        Thread.__init__(self, daemon=daemon)
        session_id = id(self)
        self.logger = create_logger(name='GAME-' + str(session_id), color='BLUE')
        self.player_1 = connection_1
        self.player_2 = connection_2

    def run(self):
        self.logger.info((
            'Game starting:' + str(self.player_1.name) +
            'VS ' + str(self.player_2.name)
        ))
        board = [['', '', ''],
                 ['', '', ''],
                 ['', '', '']]

        is_player_1_turn = True
        self.player_1.send_response({'status': 'matched'})
        self.player_2.send_response({'status': 'matched'})
        self.broadcast_board(board, is_player_1_turn)

        current_player = None

        while(self.both_players_connected()):
            current_player = (
                self.player_1 if is_player_1_turn
                else self.player_2
            )
            if current_player.command_available():
                command = current_player.pop_command()
                if BoardValidator.command_is_valid(board, command):
                    board = BoardValidator.update_board(
                        board,
                        command,
                        is_player_1_turn
                    )

                    if BoardValidator.player_won(board):
                        self.player_1.game_ended()
                        self.player_2.game_ended()
                        self.broadcast_board(
                            board,
                            is_player_1_turn,
                            winner=True
                        )
                        break

                    is_player_1_turn = not is_player_1_turn
                    self.broadcast_board(board, is_player_1_turn)

                else:
                    current_player.send_invalid_values_error()
        self.end_game_logs()

    def both_players_connected(self):
        if self.player_1.connected and self.player_2.connected:
            return True
        else:
            ERROR_MESSAGE = {
                'status': 'error',
                'error_type': 'OPPONENT_LEFT',
                'message': (
                    'Your opponent has left the game,'
                    'returning to waiting room'
                )
            }

            for player in [self.player_1, self.player_2]:
                if not player.connected:
                    self.logger.info(str(player.name) + ' has left the game...')
                player.set_waiting_match(True)
                player.send_response(ERROR_MESSAGE)

        return False

    def broadcast_board(self, board, is_player_1_turn, winner=False):
        message = {
            'status': None,
            'board': board
        }

        current = 'play'
        waiting = 'oponnent'

        if winner:
            current = 'victory'
            waiting = 'defeat'

        message['status'] = current if is_player_1_turn else waiting
        self.player_1.send_response(message)
        message['status'] = current if not is_player_1_turn else waiting
        self.player_2.send_response(message)

    def end_game_logs(self):
        self.logger.info((
            str(self.player_1.name) + ' VS ' + str(self.player_2.name) + 'game has ended'
        ))
        self.logger.info('Closing session')
