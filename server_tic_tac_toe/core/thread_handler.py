from server_tic_tac_toe.core.logger_builder import create_logger

logger = create_logger(name="THREAD", color="YELLOW")


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
    finally:
        logger.info("finishing connection")
