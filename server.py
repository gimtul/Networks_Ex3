import socket

import CONSTS

tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('localhost', 81)
tcp_socket.bind(server_address)

tcp_socket.listen(1)

while True:
    print("waiting for connection")
    connection, client = tcp_socket.accept()

    try:
        print("connected to client IP: {}".format(client))

        while True:
            data = connection.recv(CONSTS.BUFFER_SIZE)

            if data.decode() == "Max size":
                connection.sendall(str(CONSTS.BUFFER_SIZE).encode())

            if not data:
                break

            print("Recieved data: {}".format(data))

    finally:
        connection.close()
