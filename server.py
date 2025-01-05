### server.py
import socket
import CONSTS

server_address = ('localhost', 81)

# Set up the server socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind(server_address)
    server_socket.listen(1)
    print("Server is up and running, waiting for a connection...")

    while True:
        connection, client_address = server_socket.accept()
        print(f"Connected to client IP: {client_address}")

        try:
            while True:
                data = connection.recv(CONSTS.BUFFER_SIZE)
                if not data:
                    print("No data received. Closing connection.")
                    break

                message = data.decode("utf-8")
                print(f"Received data: {message}")

                if message == "Max size":
                    connection.sendall(str(CONSTS.BUFFER_SIZE).encode())
                elif message == "exit":
                    print("Client requested to close the connection.")
                    break
                else:
                    response = f"Server received: {message}"
                    connection.sendall(response.encode())

        except Exception as e:
            print(f"Error: {e}")
        finally:
            print("Closing client connection...")
            connection.close()