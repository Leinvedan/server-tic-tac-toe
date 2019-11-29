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
        self._game_ended = False

    def _encode_data(self, data):
        return bytes(data, encoding='utf8')

    def run(self):
        self.name = self._get_response_from_field(
            field_to_read='my_name',
            status_to_send='waiting'
        )
        self.logger = create_logger(name=str(self.name), color='YELLOW')
        self.is_waiting_match = True
        self.logger.info('new thread running...')

        try:
            while self.connected:
                message = self.connection.recv(1024).decode('utf8')

                if self._game_ended:
                    self._process_continue_playing(message)

                if not self.is_waiting_match:
                    self.command = self.parse_command(message)

        except Exception:
            self.logger.info('Connection broken...')
        finally:
            self.logger.info('Closing connection')
            self.close_connection()

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

    def _get_response_from_field(self, field_to_read, status_to_send=None):
        field_value = None
        try:
            response = self.connection.recv(1024).decode('utf8')
            response = json.loads(response)
            if field_to_read in response:
                field_value = response[field_to_read]
                if status_to_send:
                    self.send_response({'status': status_to_send})
        except Exception:
            self.close_connection()
        finally:
            return field_value

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
            self.logger.info('Message could not be sent:\n'+str(e))
            self.close_connection()

    def game_ended(self):
        self._game_ended = True

    def _process_continue_playing(self, message):
        try:
            response = json.loads(message)
            if 'continue' in response:
                if response['continue'] != 'y':
                    self.logger.info(str(self.name) + ' left')
                    self.close_connection()
                else:
                    self.logger.info(str(self.name) + 'still playing')
        except Exception:
            self.logger.info('Continue couldn`t be processed, ignoring...')
        finally:
            self.set_waiting_match(True)
            self._game_ended = False
