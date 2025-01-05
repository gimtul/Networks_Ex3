import socket
import time

# Client settings
HOST = 'localhost'  # Server address
PORT = 65432  # Port to connect to


def send_message_with_window(conn, message, window_size, timeout, max_msg_size):
    """
    Sends a message with sliding window logic to the server.
    """
    # Split the message into chunks of the maximum message size
    chunks = [message[i:i + max_msg_size] for i in range(0, len(message), max_msg_size)]

    # Initialize the window pointers
    start = 0
    end = min(window_size, len(chunks))  # Initial window
    sent = [False] * len(chunks)  # To track which chunks are sent and acknowledged

    while start < len(chunks):
        # Send chunks in the current window
        for i in range(start, end):
            if not sent[i]:  # Only send chunks that haven't been acknowledged
                chunk = chunks[i]
                print(f"Sending message: {chunk}")
                conn.send(chunk.encode())  # Send chunk

        # Wait for acknowledgments
        ack_received = 0  # To track how many ACKs we've received
        while ack_received < (end - start):
            conn.settimeout(timeout)  # Set timeout for acknowledgment
            try:
                data = conn.recv(1024).decode()
                if data == "ACK":
                    print(f"ACK received for chunk {start + 1 + ack_received}")
                    sent[start + ack_received] = True  # Mark this chunk as acknowledged
                    ack_received += 1  # Increment the number of acknowledged chunks
            except socket.timeout:
                print(f"Timeout waiting for ACK for chunk {start + 1 + ack_received}")
                print("Retransmitting unacknowledged chunks...")
                # Retransmit only the unacknowledged chunks
                for i in range(start, end):
                    if not sent[i]:  # Retransmit only the chunks that were not acknowledged
                        conn.send(chunks[i].encode())  # Retransmit the chunk

        # Slide the window
        start += ack_received
        end = min(start + window_size, len(chunks))

    print("All messages sent and acknowledged.")


def client_program():
    # Connect to server
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((HOST, PORT))
        print(f"Connected to server at {HOST}:{PORT}")

        # Request configuration from the server
        client_socket.send("request_max_msg_size".encode())
        max_msg_size_from_server = client_socket.recv(1024).decode()
        print(f"Max message size from server: {max_msg_size_from_server} bytes")

        client_socket.send("request_window_size".encode())
        window_size_from_server = int(client_socket.recv(1024).decode())
        print(f"Window size from server: {window_size_from_server}")

        client_socket.send("request_timeout".encode())
        timeout_from_server = int(client_socket.recv(1024).decode())
        print(f"Timeout from server: {timeout_from_server} seconds")

        # Save the configuration values
        config = {
            "max_msg_size": int(max_msg_size_from_server),
            "window_size": window_size_from_server,
            "timeout": timeout_from_server
        }

        # Print out the saved configuration
        print(f"Configuration saved: {config}")

        # Continue to send messages until the user enters 'exit'
        while True:
            # Input message to send
            message = input("Enter the message to send (or 'exit' to quit): ").strip()

            if message.lower() == "exit":
                # Send exit signal to the server and keep the connection open for future commands
                client_socket.send("exit".encode())
                print("Exiting...")
                break  # Break out of the loop to close the connection

            # Send the message with sliding window mechanism
            send_message_with_window(client_socket, message, config["window_size"], config["timeout"],
                                     config["max_msg_size"])

        print("Connection closed.")


if __name__ == "__main__":
    client_program()
