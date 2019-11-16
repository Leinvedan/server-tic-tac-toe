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

                if not self.connected:
                    break

        except Exception:
            self.close_connection()
            self.logger.info('Connection broken...')
        finally:
            self.logger.info('Closing connection')

    def set_waiting_match(self, is_waiting):
        self.is_waiting_match = is_waiting

    def pop_command(self):
        command, self.command = self.command, None
        return command

    def command_available(self):
        return bool(self.command)

    def close_connection(self):
        self.connected = False
        self.connection.close()

    def get_user_name(self):
        name = self.connection.recv(1024).decode('utf8')
        self.send_response({
            'status': 'waiting',
            'message': f'Welcome {name}!\nWaiting for player 2'
        })
        return name

    def parse_response(self, message):
        try:
            jsonObj = json.loads(message)
            if 'line' in jsonObj and 'column' in jsonObj:
                return Command(
                    line=int(jsonObj['line']),
                    column=int(jsonObj['column'])
                )
            return None
        except Exception:
            self.send_response({
                'status': 'error',
                'message': ('Invalid format!'
                            'expected JSON with line and column fields'
                            )
            })

    def send_response(self, message):
        try:
            if self.connected:
                message = json.dumps(message)
                self.connection.sendall(self._encode_data(message))
        except Exception as e:
            self.logger.info(f'Message could not be sent:\n{e}')
            self.close_connection()
