import json
from threading import Thread
from collections import namedtuple

from server_tic_tac_toe.utils.logger_builder import create_logger

Command = namedtuple('command', 'line column')


class ConnectionHandler(Thread):
    def __init__(self, connection, client, daemon=True):
        Thread.__init__(self, daemon=daemon)
        self.connection = connection
        self.client = client
        self.connected = True
        self.is_waiting_match = False
        self.command = None

    def _encode_data(self, data):
        return bytes(data, encoding='utf8')

    def run(self):
        self.name = self.get_user_name()
        self.logger = create_logger(name=f'{self.name}', color='YELLOW')
        self.is_waiting_match = True

        self.logger.info('new thread running...')
        try:
            while True:
                message = self.connection.recv(1024).decode('utf8')
                if not self.is_waiting_match:
                    self.command = self.parse_response(message)
                else:
                    self.send_response('Please wait another player to join')

                if not self.connected:
                    break

        except Exception:
            self.close_connection()
            self.logger.info('Something went wrong... closing connection')
        finally:
            self.logger.info('finishing connection')

    def set_playing(self):
        self.is_waiting_match = False

    def get_command(self):
        return self.command

    def close_connection(self):
        self.connected = False
        self.connection.close()

    def get_user_name(self):
        name = self.connection.recv(1024).decode('utf8')
        self.connection.sendall(
            bytes(
                f'Welcome {name}!\nWaiting for player 2',
                encoding='utf8'
                )
            )
        return name

    def parse_response(self, message):
        self.logger.info(message)
        try:
            jsonObj = json.loads(message)
            if jsonObj and jsonObj['line'] and jsonObj['column']:
                com = Command(
                    line=int(jsonObj['line']),
                    column=int(jsonObj['column'])
                )
                self.logger.info(com)
                return com
            return None
        except Exception:
            self.send_response(
                'Invalid format!\nexpected JSON with line and column fields'
            )

    def send_response(self, message, clear_command=False):
        self.connection.send(self._encode_data(message))
