import socket
import CONSTS

def divide_message(message, max_size):
    """Divide the message into chunks of max_size."""
    return [message[i:i+max_size] for i in range(0, len(message), max_size)]

server_address = ('localhost', 81)

# Connect to the server
with socket.create_connection(server_address) as tcp_socket:
    try:
        tcp_socket.sendall("Max size".encode())
        max_size = int(tcp_socket.recv(CONSTS.BUFFER_SIZE).decode())
        print(f"Server buffer size: {max_size}")

        while True:
            data = input("Enter message (type 'exit' to close): ")

            if data == "exit":
                tcp_socket.sendall(data.encode())
                print("Exiting client...")
                break

            try:
                encoded_data = data.encode("utf-8")
                if len(encoded_data) <= max_size:
                    tcp_socket.sendall(encoded_data)
                else:
                    chunks = divide_message(data, max_size)
                    for chunk in chunks:
                        tcp_socket.sendall(chunk.encode("utf-8"))

                response = tcp_socket.recv(CONSTS.BUFFER_SIZE).decode()
                print(f"Response from server: {response}")

            except Exception as e:
                print(f"Error during communication: {e}")

    except Exception as e:
        print(f"Error connecting to server: {e}")

    finally:
        print("Connection closed.")