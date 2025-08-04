import asyncio

default_host = "127.0.0.1"
host_input = input(f"Enter server host to bind to (default: {default_host}): ").strip()
HOST = host_input if host_input else default_host
PORT = 5000

connected_clients = set()

async def handle_client(reader, writer):
    addr = writer.get_extra_info('peername')
    connected_clients.add(addr)
    print(f"Connected by {addr}")

    try:
        while True:
            data = await reader.read(1024)
            if not data:
                print(f"Disconnected by {addr}")
                break

            message = data.decode().strip()

            if message == "list":
                client_list = "\n".join(f"{client}" for client in connected_clients)
                response = f"Connected clients:\n{client_list}\n"
                writer.write(response.encode())
                await writer.drain()
                continue  # Skip echoing the original message

            print(f"Received {message} from {addr}")
            writer.write(data)
            await writer.drain()
    except ConnectionResetError:
        print(f"Client {addr} forcibly closed the connection.")
    finally:
        connected_clients.discard(addr)
        writer.close()
        await writer.wait_closed()


async def command_listener():
    while True:
        cmd = await asyncio.get_event_loop().run_in_executor(None, input, "> ")
        if cmd.strip().lower() == "list":
            if connected_clients:
                print("Connected clients:")
                for client in connected_clients:
                    print(f" - {client}")
            else:
                print("No clients connected.")
        else:
            print("Unknown command. Use 'list' to see connected clients.")

async def main():
    try:
        server = await asyncio.start_server(handle_client, HOST, PORT)
        print(f"Server listening on {HOST}:{PORT}")

        # Run both the server and command listener concurrently
        await asyncio.gather(
            server.serve_forever(),
            command_listener()
        )

    except Exception as e:
        print(f"Failed to start server on {HOST}:{PORT} — {e}")

asyncio.run(main())
