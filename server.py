import asyncio

default_host = "test.reverberver.online"
host_input = input(f"Enter server host to bind to (default: {default_host}): ").strip()
HOST = host_input if host_input else default_host
PORT = 5000

connected_clients = {}  # Maps client_name -> (reader, writer)
client_lock = asyncio.Lock()

async def handle_client(reader, writer):
    addr = writer.get_extra_info('peername')

    # Receive the client's name first
    name_data = await reader.read(1024)
    client_name = name_data.decode().strip()

    if not client_name:
        writer.write(b"Name cannot be empty.\n")
        await writer.drain()
        writer.close()
        await writer.wait_closed()
        return

    async with client_lock:
        if client_name in connected_clients:
            writer.write(b"Name already taken. Disconnecting.\n")
            await writer.drain()
            writer.close()
            await writer.wait_closed()
            return

        connected_clients[client_name] = (reader, writer)

    print(f"{client_name} connected from {addr}")
    writer.write(f"Welcome {client_name}! Use 'list' to see clients, 'to <ClientX>: message' to send.\n".encode())
    await writer.drain()


    try:
        while True:
            data = await reader.read(1024)
            if not data:
                print(f"{client_name} disconnected")
                break

            message = data.decode().strip()

            if message.lower() == "list":
                client_list = "\n".join([f"{name}{' (you)' if name == client_name else ''}" for name in connected_clients])
                response = f"Connected clients:\n{client_list}\n"
                writer.write(response.encode())
                await writer.drain()
                continue

            if message.lower().startswith("to "):
                try:
                    header, msg = message.split(":", 1)
                    _, target_name = header.strip().split(" ", 1)
                    msg = msg.strip()
                except ValueError:
                    writer.write(b"Invalid message format. Use: to <ClientName>: <message>\n")
                    await writer.drain()
                    continue

                if target_name not in connected_clients:
                    writer.write(f"No client named '{target_name}'\n".encode())
                    await writer.drain()
                    continue

                _, target_writer = connected_clients[target_name]
                target_writer.write(f"{client_name} says: {msg}\n".encode())
                await target_writer.drain()
                writer.write(b"Message sent.\n")
                await writer.drain()
            else:
                writer.write(b"Unknown command or invalid format.\n")
                await writer.drain()

    except ConnectionResetError:
        print(f"{client_name} forcibly closed the connection.")
    finally:
        async with client_lock:
            connected_clients.pop(client_name, None)
        writer.close()
        await writer.wait_closed()

async def command_listener():
    while True:
        cmd = await asyncio.get_event_loop().run_in_executor(None, input, "> ")
        if cmd.strip().lower() == "list":
            if connected_clients:
                print("Connected clients:")
                for name in connected_clients:
                    print(f" - {name}")
            else:
                print("No clients connected.")
        else:
            print("Unknown command. Use 'list' to see connected clients.")

async def main():
    try:
        server = await asyncio.start_server(handle_client, HOST, PORT)
        print(f"Server listening on {HOST}:{PORT}")

        await asyncio.gather(
            server.serve_forever(),
            command_listener()
        )

    except Exception as e:
        print(f"Failed to start server on {HOST}:{PORT} — {e}")

asyncio.run(main())
