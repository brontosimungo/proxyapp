from fastapi import FastAPI, WebSocket
import asyncio
import socket

app = FastAPI()

@app.websocket("/ws")
async def websocket_proxy(websocket: WebSocket):
    await websocket.accept()
    
    # koneksi ke backend
    backend = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    backend.connect(("127.0.0.1", 3306))

    try:
        while True:
            data = await websocket.receive_bytes()
            backend.sendall(data)
            response = backend.recv(4096)
            await websocket.send_bytes(response)
    except Exception as e:
        await websocket.close()
        backend.close()
