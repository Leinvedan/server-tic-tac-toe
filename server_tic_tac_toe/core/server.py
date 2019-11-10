import socket
from threading import Thread

from server_tic_tac_toe.core.logger_builder import create_logger
from server_tic_tac_toe.core.thread_handler import handle_connection

HOST = 'localhost'
PORT = 5332
logger = create_logger(name="SERVER", color="CYAN")


def open_tcp_server_socket():
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    tcp.bind((HOST, PORT))
    tcp.listen(1)
    return tcp


tcp = open_tcp_server_socket()
logger.info('Listening...')
while True:
    try:
        connection, client = tcp.accept()
        logger.info(client)
        connection_handler = Thread(
            target=handle_connection,
            args=(connection, client),
            daemon=True
        )
        connection_handler.start()
    except KeyboardInterrupt:
        tcp.shutdown(socket.SHUT_RDWR)
        tcp.close()
        logger.info("Exiting...")
        break


