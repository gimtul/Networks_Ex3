import socket

import CONSTS


server_address = ('localhost', 81)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:

    server_socket.bind(server_address)
    server_socket.listen(1)

    while True:
        print("waiting for connection")
        connection, client = server_socket.accept()

        try:
            print("connected to client IP: {}".format(client))

            data = connection.recv(CONSTS.BUFFER_SIZE)

            if data.decode() == "Max size":
                connection.sendall(str(CONSTS.BUFFER_SIZE).encode())

            if not data:
                break

            print("Recieved data: {}".format(data))
        except KeyboardInterrupt:
            print("Shutting down...")
            break

