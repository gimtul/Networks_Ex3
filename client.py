import socket

# Client settings
HOST = 'localhost'  # Server address
PORT = 65432  # Port to connect to


def send_message_with_window(conn, message, window_size, timeout, max_msg_size):
    chunks = [message[i:i + max_msg_size] for i in range(0, len(message), max_msg_size)]

    start = 0
    end = min(window_size, len(chunks))
    sent = [False] * len(chunks)

    while start < len(chunks):
        for i in range(start, end):
            if not sent[i]:
                chunk = f"{i}:{chunks[i]}\n"  # Add sequence number and delimiter
                print(f"Sending message: {chunk.strip()}")
                conn.send(chunk.encode())

        ack_received = 0
        while ack_received < (end - start):
            conn.settimeout(timeout)
            try:
                data = conn.recv(1024).decode()
                print(f"Received data: {data}")

                # Process the data by splitting it into individual ACKs
                while "ACK" in data:
                    ack_index = data.find("ACK")
                    print(f"ACK received for chunk {start + ack_received}")
                    sent[start + ack_received] = True
                    ack_received += 1
                    data = data[ack_index + 3:]  # Remove the processed "ACK"

            except socket.timeout:
                print(f"Timeout waiting for ACK for chunk {start + ack_received}")
                print("Retransmitting unacknowledged chunks...")
                for i in range(start, end):
                    if not sent[i]:
                        chunk = f"{i}:{chunks[i]}\n"
                        conn.send(chunk.encode())

        start += ack_received
        end = min(start + window_size, len(chunks))

    print("All messages sent and acknowledged.")


def client_program():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((HOST, PORT))
        print(f"Connected to server at {HOST}:{PORT}")

        client_socket.send("request_max_msg_size\n".encode())
        max_msg_size_from_server = client_socket.recv(1024).decode()

        client_socket.send("request_window_size\n".encode())
        window_size_from_server = int(client_socket.recv(1024).decode())

        client_socket.send("request_timeout\n".encode())
        timeout_from_server = int(client_socket.recv(1024).decode())

        config = {
            "max_msg_size": int(max_msg_size_from_server),
            "window_size": window_size_from_server,
            "timeout": timeout_from_server
        }

        while True:
            message = input("Enter the message to send (or 'exit' to quit): ").strip()
            if message.lower() == "exit":
                client_socket.send("exit\n".encode())
                break
            send_message_with_window(
                client_socket, message, config["window_size"], config["timeout"], config["max_msg_size"]
            )

        print("Connection closed.")


if __name__ == "__main__":
    client_program()
