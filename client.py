import socket

DEFAULT_HOST = "127.0.0.1"
HOST_INPUT = input(f"Enter server host (default: {DEFAULT_HOST}): ").strip()
HOST = HOST_INPUT if HOST_INPUT else DEFAULT_HOST
PORT = 5000

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    print("Connected to the server. Type messages and press Enter to send. Type 'quit' to exit.")
    
    while True:
        message = input("You: ")
        if message.lower() == "quit":
            print("Closing connection.")
            break
        if not message.strip():
            print("Empty message")
            continue

        s.sendall(message.encode())
        data = s.recv(1024)
        print(f"Server: {data.decode()}")
