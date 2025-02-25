import json
import ccxt
import websockets
from fastapi import WebSocket
from typing import List


class WebSocketManager:
    """Manages active WebSocket connections."""

    def __init__(self):
        self._active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        """Accepts new WebSocket connection."""
        await websocket.accept()
        self._active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        """Removes disconnected WebSocket connection."""
        self._active_connections.remove(websocket)

    async def broadcast(self, message: str):
        """Sends a message to all connected clients."""
        for connection in self._active_connections:
            try:
                await connection.send_text(message)
            except:
                self.disconnect(connection)

    @property
    def active_connections(self):
        return self._active_connections


manager = WebSocketManager()


async def binance_websocket(crypto_list):
    """Fetches live prices from Binance WebSocket API and broadcasts to clients."""
    url = f"wss://stream.binance.com:9443/ws/{'/'.join([c.lower() + 'usdt@ticker' for c in crypto_list])}"

    async with websockets.connect(url) as websocket:
        while True:
            data = json.loads(await websocket.recv())

            symbol = data['s'].replace("USDT", "").lower()
            price = data['c']
            change = data['P']

            update = {
                "short": symbol,
                "long": symbol.upper(),
                "price": price,
                "change": change,
            }

            await manager.broadcast(json.dumps(update))


