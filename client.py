import socket
import CONSTS


def divideMessage():
    print("hello")


tcp_socket = socket.create_connection(('localhost', 81))

try:
    tcp_socket.sendall(str.encode("Max size"))
    maxSize = tcp_socket.recv(CONSTS.BUFFER_SIZE).decode()
    print(maxSize)
finally:
    while True:
        data = input()
        try:


            if data == "exit":
                break

            try:
                encodedData = data.encode("utf-8")
                if len(encodedData) <= int(maxSize):
                    tcp_socket.sendall(encodedData)
                else:
                    divideMessage()

                response = tcp_socket.recv(CONSTS.BUFFER_SIZE).decode()
                print(response)
            finally:
                print("hey")

        finally:
            print("closed")
