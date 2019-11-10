import socket
from threading import Thread

from server_tic_tac_toe.utils.logger_builder import create_logger
from server_tic_tac_toe.server.protocols import open_tcp_server_socket
from server_tic_tac_toe.server.connection_handler import ConnectionHandler


logger = create_logger(name="SERVER", color="CYAN")


tcp = open_tcp_server_socket()
logger.info('Listening...')
player_counter = 0

while True:
    try:
        connection, client = tcp.accept()
        logger.info(f'connected to: {str(client)}')
        player_counter += 1

        connection_handler = ConnectionHandler(
            connection=connection,
            client=client,
            name=player_counter
        ) 
        connection_handler.start()

    except KeyboardInterrupt as e:
        tcp.shutdown(socket.SHUT_RDWR)
        tcp.close()
        logger.info('Closing server...')
        break
    except InterruptedError:
        logger.info('New connection interrupted')
    except Exception as e:
        logger.info(f'Something went wrong:{e}')
