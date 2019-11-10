import socket

from server_tic_tac_toe.config import HOST, PORT


def open_tcp_server_socket():
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    tcp.bind((HOST, PORT))
    tcp.listen(1)
    return tcp
