from server_tic_tac_toe.utils.logger_builder import create_logger


def encode_data(data):
    return bytes(data, encoding='utf8')


def handle_connection(connection, client, name):
    logger = create_logger(name=f'THREAD-{name}', color='YELLOW')
    logger.info('new thread running...')
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
        logger.info('finishing connection')
