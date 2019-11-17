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
            while self.connected:
                message = self.connection.recv(1024).decode('utf8')
                if not self.is_waiting_match:
                    self.command = self.parse_command(message)

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
        name = None
        try:
            response = self.connection.recv(1024).decode('utf8')
            response = json.loads(response)
            if 'my_name' in response:
                name = response['my_name']
                self.send_response({'status': 'waiting'})
        except Exception:
            self.close_connection()
        finally:
            return name

    def parse_command(self, message):
        command = None
        try:
            jsonObj = json.loads(message)
            if 'line' in jsonObj and 'column' in jsonObj:
                command = Command(
                    line=int(jsonObj['line']),
                    column=int(jsonObj['column'])
                )

        except Exception:
            command = None
            self.send_invalid_format_error()

        finally:
            return command

    def send_invalid_format_error(self):
        self.send_response({
            'status': 'error',
            'error_type': 'INVALID_FORMAT',
            'message': ('Invalid format!'
                        'expected line and column fields '
                        'with INTEGER values'
                        )
        })

    def send_invalid_values_error(self):
        self.send_response({
            'status': 'error',
            'error_type': 'INVALID_VALUES',
            'message': ('Invalid values!'
                        'The taget position must be empty,'
                        ' and the values between 1 and 3.'
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
