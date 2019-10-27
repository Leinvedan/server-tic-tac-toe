import socket

#testing client

def read_input_as_bytes():
  return bytes(input(">"), encoding='utf8')


HOST = 'localhost'
PORT = 5332
try:
  tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  dest = (HOST, PORT)
  tcp.connect(dest)

  print("Write message:")
  message_to_send = read_input_as_bytes()
  while message_to_send != "quit":
    tcp.sendall(message_to_send)
    response = tcp.recv(1024)
    print("server:",response.decode('utf8'))
    message_to_send = read_input_as_bytes()
except KeyboardInterrupt:
    print("Exiting...")
finally:
  tcp.close()
