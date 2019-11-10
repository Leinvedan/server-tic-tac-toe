from threading import Thread

from server_tic_tac_toe.utils.logger_builder import create_logger

class PlayerMatcher(Thread):
    def __init__(self, daemon=True):
        Thread.__init__(self, daemon=daemon)
        self.logger = create_logger(name=f'MATCHER', color='GREEN')
        self.player_list = []

    def get_player_list(self):
        return self.player_list

    def add_new_player(self, new_connection):
        self.player_list.append(new_connection)

    def run(self):
        self.logger.info('Player Matcher started...')
        while True:
            paired_players = []
            for index, player in enumerate(self.player_list):
                if player:
                    if not player.connected:
                        del self.player_list[index]
                    elif player.is_waiting_match:
                        paired_players.append(player)
                        if len(paired_players) == 2:
                            self.logger.info('Players matched!')
                            paired_players[0].set_playing()
                            paired_players[1].set_playing()