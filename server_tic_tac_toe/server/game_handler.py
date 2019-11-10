from threading import Thread
from server_tic_tac_toe.utils.logger_builder import create_logger


class GameHandler(Thread):
    def __init__(self, player_1, player_2, daemon=True):
        Thread.__init__(self, daemon=daemon)
        self.logger = create_logger(name=f'GAME', color='BLUE')
        self.player_1 = player_1
        self.player_2 = player_2

    def run(self):
        self.logger.info(
            f'Game starting:{self.player_1.name} VS {self.player_2.name}'
        )
        self.player_1.set_playing()
        self.player_2.set_playing()
