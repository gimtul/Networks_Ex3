import socket
import CONSTS

tcp_socket = socket.create_connection(('localhost', 81))

try:
    tcp_socket.sendall(str.encode("Max size"))
    response = tcp_socket.recv(CONSTS.BUFFER_SIZE).decode()
    print(response)
finally:
    while True:

        try:
            data = input()

            if data == "exit":
                break

            while True:

                tcp_socket.sendall(data.encode())

                response = tcp_socket.recv(CONSTS.BUFFER_SIZE).decode()
                print(response)

        finally:
            print("closed")
