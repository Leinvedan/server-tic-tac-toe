from threading import Thread

from server_tic_tac_toe.utils.logger_builder import create_logger


class ConnectionHandler(Thread):
  def __init__(self, connection, client, name, daemon=True):
    Thread.__init__(self, daemon=daemon)
    self.connection = connection
    self.client = client
    self.name = name
    self.logger = create_logger(name=f'THREAD-{name}', color='YELLOW')

  def _encode_data(self, data):
    return bytes(data, encoding='utf8')

  def run(self):
    self.logger.info('new thread running...')
    try:
        while True:
            message = self.connection.recv(1024).decode('utf8')
            if not message:
                break
            self.logger.info(message)
            self.connection.send(self._encode_data('sup'))
        self.connection.close()
    except Exception:
        self.connection.close()
    finally:
        self.logger.info('finishing connection')




