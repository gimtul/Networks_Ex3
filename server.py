import socket

# Server settings
HOST = 'localhost'  # Host address
PORT = 65432         # Port to listen on

received_chunks = {}

def read_config(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            config = {}
            for line in f:
                key, value = line.strip().split(":", 1)
                config[key.strip()] = value.strip().strip('"')
            return config
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return None
    except Exception as e:
        print(f"Error reading configuration file: {e}")
        return None



def get_server_config():
    print("Choose configuration input method:")
    print("1. Manual input")
    print("2. From a file")
    choice = input("Enter your choice (1 or 2): ").strip()

    if choice == "1":
        try:
            maximum_msg_size = int(input("Enter the maximum message size (in bytes): ").strip())
            window_size = int(input("Enter the window size (number of messages in a window): ").strip())
            timeout = int(input("Enter the timeout (in seconds): ").strip())
            return {
                "maximum_msg_size": maximum_msg_size,
                "window_size": window_size,
                "timeout": timeout
            }
        except ValueError:
            print("Invalid input. Please ensure all values are entered correctly.")
            exit(1)
    elif choice == "2":
        file_path = input("Enter the path to the configuration file: ").strip()
        config = read_config(file_path)
        if config is None:
            print("Failed to read configuration from file. Exiting.")
            exit(1)
        return {
            "maximum_msg_size": int(config.get("maximum_msg_size", 0)),
            "window_size": int(config.get("window_size", 0)),
            "timeout": int(config.get("timeout", 0))
        }
    else:
        print("Invalid choice. Exiting.")
        exit(1)


def server_program():
    config = get_server_config()
    maximum_msg_size = config["maximum_msg_size"]
    window_size = config["window_size"]
    timeout = config["timeout"]

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen(1)
        print(f"Server is listening on {HOST}:{PORT}...")

        conn, addr = server_socket.accept()
        with conn:
            print(f"Connected by {addr}")
            buffer = ""  # Buffer to store incomplete data
            expected_seq_num = 0
            while True:
                data = conn.recv(1024).decode()
                if not data:
                    break

                buffer += data
                while '\n' in buffer:
                    message, buffer = buffer.split('\n', 1)
                    if message.lower() == "request_max_msg_size":
                        conn.send(str(maximum_msg_size).encode())
                    elif message.lower() == "request_window_size":
                        conn.send(str(window_size).encode())
                    elif message.lower() == "request_timeout":
                        conn.send(str(timeout).encode())
                    elif ":" in message:
                        # Parse the sequence number and the chunk
                        seq_num, chunk = message.split(":", 1)
                        seq_num = int(seq_num)
                        print(f"Received chunk {seq_num}: {chunk}")
                        # Store the chunk in the received_chunks dictionary
                        received_chunks[seq_num] = chunk
                        # Check for missing chunks
                        missing_chunks = [i for i in range(expected_seq_num, seq_num) if i not in received_chunks]
                        if missing_chunks:
                            # If missing chunks exist, ask for retransmission of the missing chunks
                            print(f"Missing chunks: {missing_chunks}")
                            conn.send(f"RETRY:{','.join(map(str, missing_chunks))}\n".encode())
                        else:
                            # Once all chunks up to the current seq_num are received, acknowledge the chunk
                            print(f"ACK for chunk {seq_num}")
                            conn.send("ACK\n".encode())
                            # Move to the next expected chunk
                            expected_seq_num = seq_num + 1
                        conn.send("ACK".encode())
                    elif message.lower() == "exit":
                        print("Client requested to exit. Closing connection.")
                        return
                    else:
                        print(f"Unrecognized message: {message}")
                        conn.send("ACK".encode())


if __name__ == "__main__":
    server_program()
