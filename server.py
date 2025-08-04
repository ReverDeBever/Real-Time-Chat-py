import asyncio

default_host = "127.0.0.1"
host_input = input(f"Enter server host to bind to (default: {default_host}): ").strip()
HOST = host_input if host_input else default_host
PORT = 5000

async def handle_client(reader, writer):
    addr = writer.get_extra_info('peername')
    print(f"Connected by {addr}")

    while True:
        data = await reader.read(1024)
        if not data:
            print(f"Disconnected by {addr}")
            break
        print(f"Received {data.decode()} from {addr}")
        writer.write(data)
        await writer.drain()

    writer.close()
    await writer.wait_closed()

async def main():
    try:
        server = await asyncio.start_server(handle_client, HOST, PORT)
        print(f"Server listening on {HOST}:{PORT}")

        async with server:
            await server.serve_forever()
    except Exception as e:
        print(f"Failed to start server on {HOST}:{PORT} — {e}")

asyncio.run(main())
