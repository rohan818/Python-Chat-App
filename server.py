import asyncio
import websockets

# To keep track of all connected clients
connected_clients = set()

async def handle_client(websocket, path):
    connected_clients.add(websocket)

    try:
        async for message in websocket:
            for client in connected_clients:
                if client != websocket:
                    await client.send(message)
    finally:
        connected_clients.remove(websocket)

async def main():
    async with websockets.serve(handle_client, "localhost", 12345):
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())