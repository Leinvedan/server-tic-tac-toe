import socket

from server_tic_tac_toe.utils.logger_builder import create_logger
from server_tic_tac_toe.server.protocols import open_tcp_server_socket
from server_tic_tac_toe.server.connection_handler import ConnectionHandler
from server_tic_tac_toe.server.player_matcher import PlayerMatcher

logger = create_logger(name="SERVER", color="CYAN")


tcp = open_tcp_server_socket()
logger.info('Listening...')

player_matcher = PlayerMatcher()
player_matcher.start()

while True:
    try:
        connection, client = tcp.accept()
        logger.info('connected to:' + str(client))

        player_connection = ConnectionHandler(
            connection=connection,
            client=client
        )
        player_connection.start()
        player_matcher.add_new_player(player_connection)

    except KeyboardInterrupt:
        tcp.shutdown(socket.SHUT_RDWR)
        tcp.close()
        logger.info('Closing server...')
        break
    except InterruptedError:
        logger.info('New connection interrupted')
    except Exception as e:
        logger.info('Something went wrong:' + str(e))
