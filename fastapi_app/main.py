import os
import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse
from fastapi_app.websocket_app import manager as ws_manager, binance_websocket

import django

# Set the Django settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "TiluBee.settings")
django.setup()
from payment_utils.tickers import COINS_DICT


app = FastAPI()

@app.get("/")
def root():
    return JSONResponse({"message": "Hello Sssss from FastAPI!"})

@app.get("/home")
def home():
    return JSONResponse({"message": "Hello Sosthenes from FastAPI!"})











@app.websocket("/tickers")
async def websocket_endpoint(websocket: WebSocket):
    """Handles WebSocket connections."""
    await ws_manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()  # Keep connection alive
            if ws_manager.active_connections:
                await binance_websocket(list(COINS_DICT))
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket)

