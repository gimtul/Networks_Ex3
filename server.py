import socket

# Server settings
HOST = 'localhost'  # Host address
PORT = 65432         # Port to listen on

def read_config(file_path):
    """
    Reads configuration file and returns the required variables.
    """
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
    """
    Allows the user to choose how to input server configuration.
    Returns a dictionary with the configuration.
    """
    print("Choose configuration input method:")
    print("1. Manual input")
    print("2. From a file")
    choice = input("Enter your choice (1 or 2): ").strip()

    if choice == "1":
        # Manual input for all variables
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
        # File input
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
    # Get server configuration
    config = get_server_config()
    maximum_msg_size = config["maximum_msg_size"]
    window_size = config["window_size"]
    timeout = config["timeout"]

    # Start the server
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen(1)
        print(f"Server is listening on {HOST}:{PORT}...")

        conn, addr = server_socket.accept()
        with conn:
            print(f"Connected by {addr}")
            while True:
                data = conn.recv(1024).decode()
                if not data:
                    break

                print(f"Received: {data}")

                if data.lower() == "request_max_msg_size":
                    # Send the maximum message size to the client
                    conn.send(str(maximum_msg_size).encode())
                elif data.lower() == "request_window_size":
                    # Send the window size to the client
                    conn.send(str(window_size).encode())
                elif data.lower() == "request_timeout":
                    # Send the timeout to the client
                    conn.send(str(timeout).encode())
                elif data.lower() == "exit":
                    print("Client requested to exit. Closing connection.")
                    break
                else:
                    # Acknowledge receipt of other data
                    conn.send("ACK".encode())

if __name__ == "__main__":
    server_program()
