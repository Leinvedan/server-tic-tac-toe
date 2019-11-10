import logging

COLORS = {
    'RED': '\u001b[31m',
    'CYAN': '\u001b[36m',
    'YELLOW': '\u001b[33m',
    'GREEN': '\u001b[32m',
    'BLUE': '\u001b[34m',
    'RESET': '\033[0m'
}

logging.basicConfig(format='[%(name)s]:%(message)s', level=logging.DEBUG)


def create_logger(name, color):
    colored_name = COLORS[color] + name + COLORS["RESET"]
    logger = logging.getLogger(colored_name)
    return logger
