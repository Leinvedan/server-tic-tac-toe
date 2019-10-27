import socket
from threading import Thread
import logging

HOST = 'localhost'
PORT = 5332
logger = logging.getLogger("SERVER")
logging.basicConfig(level=logging.INFO)

def encode_data(data):
  return bytes(data, encoding='utf8')


def handle_connection(connection, client):
  logger.info("new thread running...")
  try:
    while True:
      message = connection.recv(1024).decode('utf8')
      if not message:
        break
      logger.info(message)
      connection.send(encode_data('sup'))
    connection.close()
  except Exception:
    connection.close()


try:
  tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  tcp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

  tcp.bind((HOST, PORT))
  tcp.listen(1)
  logger.info("Listening...")

  while True:
    connection, client = tcp.accept()
    logger.info(client)
    connection_handler = Thread(target=handle_connection, args=(connection, client), daemon=True)
    connection_handler.start()

except KeyboardInterrupt:
  tcp.shutdown(socket.SHUT_RDWR)
  tcp.close()
  logger.info("Exiting...")