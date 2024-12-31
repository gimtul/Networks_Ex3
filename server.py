import socket

tcp_socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('localhost', 81)
tcp_socket.bind(server_address)

tcp_socket.listen(1)

while True:
    print("waiting for connection")
    connection, client=tcp_socket.accept()

    try:
        print("connected to client IP: {}".format(client))

        while True:
            data = connection.recv(32)
            print("Recieved data: {}".format(data))
            
            if not data:
                break
    finally:
        connection.close()