import socket
import threading

DEFAULT_HOST = "127.0.0.1"
HOST_INPUT = input(f"Enter server host (default: {DEFAULT_HOST}): ").strip()
HOST = HOST_INPUT if HOST_INPUT else DEFAULT_HOST
PORT = 5000

target_client = None  # Who we're chatting with

def receive_messages(sock):
    while True:
        try:
            data = sock.recv(1024)
            if not data:
                print("\n[Disconnected from server]")
                break
            print(f"\n{data.decode()}\nYou: ", end="", flush=True)
        except Exception:
            break

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))

    name = input("Enter your name: ").strip()
    while not name:
        name = input("Name cannot be empty. Enter your name: ").strip()
    s.sendall(name.encode())

    threading.Thread(target=receive_messages, args=(s,), daemon=True).start()

    print("Commands:\n  list - show connected users\n  select <name> - choose person to chat\n  stop - stop chatting\n  exit - close client")

    while True:
        message = input("You: ").strip()

        if message.lower() == "exit":
            print("Closing connection.")
            break

        elif message.lower() == "list":
            s.sendall(b"list")

        elif message.lower().startswith("select "):
            parts = message.split(" ", 1)
            if len(parts) == 2 and parts[1].strip():
                target_client = parts[1].strip()
                print(f"[You are now chatting with {target_client}]")
            else:
                print("Usage: select <ClientName>")

        elif message.lower() == "stop":
            if target_client:
                print(f"[Left chat with {target_client}]")
                target_client = None
            else:
                print("You’re not in a conversation.")

        elif not message:
            continue

        elif target_client:
            # Automatically format message
            full_msg = f"to {target_client}: {message}"
            s.sendall(full_msg.encode())

        else:
            print("You're not in a chat. Use 'list' and 'select <name>' first.")
