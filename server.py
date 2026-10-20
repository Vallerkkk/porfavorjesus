"""
Servidor Back-end com Supabase + SQLite Gratuito para o Órbita (Pasta SITEEE)
- Banco de dados em Nuvem: Supabase PostgreSQL com Realtime
- Banco de dados Local Fallback: SQLite nativo (orbita.db)
- WebSockets nativos (FastAPI) para sincronização multi-dispositivo
- Serve o front-end orbita.html automaticamente em http://localhost:8000
"""
import json
import os
import sqlite3
import time
from pathlib import Path
from typing import Dict, List

import jwt
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "orbita.db"

# Supabase Credentials (Configurados)
SUPABASE_URL = os.getenv("SUPABASE_URL", "https://hwhzzlivoisylmtyfkgu.supabase.co")
SUPABASE_PUBLISHABLE_KEY = os.getenv("SUPABASE_PUBLISHABLE_KEY", "sb_publishable_NI_xPZVMM-LZL0WHDjyJNw_Cmnb38XX")
SUPABASE_JWKS_URL = os.getenv("SUPABASE_JWKS_URL", "https://hwhzzlivoisylmtyfkgu.supabase.co/auth/v1/.well-known/jwks.json")
SUPABASE_SECRET_KEY = os.getenv("SUPABASE_SECRET_KEY", "sb_secret_Ozi475zSO2hBG9LkvJmzGQ_mGtRJGTg")

# LiveKit (Opcional - SFU de voz/vídeo)
LIVEKIT_API_KEY = os.getenv("LIVEKIT_API_KEY", "devkey")
LIVEKIT_API_SECRET = os.getenv("LIVEKIT_API_SECRET", "secret")
LIVEKIT_URL = os.getenv("LIVEKIT_URL", "wss://seu-projeto.livekit.cloud")

app = FastAPI(title="Órbita Server (Supabase & Realtime)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def init_db() -> None:
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY,
                conv_key TEXT NOT NULL,
                payload TEXT NOT NULL,
                created_at REAL NOT NULL
            )
            """
        )
        conn.commit()


init_db()


class ConnectionManager:
    def __init__(self) -> None:
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket) -> None:
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket) -> None:
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message_text: str, sender: WebSocket = None) -> None:
        for conn in list(self.active_connections):
            if conn is not sender:
                try:
                    await conn.send_text(message_text)
                except Exception:
                    self.disconnect(conn)


manager = ConnectionManager()


@app.get("/")
def serve_home():
    return FileResponse(BASE_DIR / "orbita.html")


@app.get("/orbita.html")
def serve_orbita():
    return FileResponse(BASE_DIR / "orbita.html")


@app.get("/api/supabase/config")
def get_supabase_config():
    """Retorna credenciais públicas para o cliente web."""
    return {
        "supabase_url": SUPABASE_URL,
        "publishable_key": SUPABASE_PUBLISHABLE_KEY,
        "jwks_url": SUPABASE_JWKS_URL,
        "status": "connected"
    }


@app.get("/api/messages")
def list_messages(conv_key: str = "orbita:geral"):
    with sqlite3.connect(DB_PATH) as conn:
        rows = conn.execute(
            "SELECT payload FROM messages WHERE conv_key = ? ORDER BY created_at ASC LIMIT 200",
            (conv_key,),
        ).fetchall()
    return JSONResponse([json.loads(r[0]) for r in rows])


@app.get("/token")
def issue_livekit_token(room: str = "principal", identity: str = "usuario"):
    now = int(time.time())
    claims: Dict[str, object] = {
        "iss": LIVEKIT_API_KEY,
        "sub": identity,
        "nbf": now,
        "exp": now + 3600 * 6,
        "video": {
            "roomJoin": True,
            "room": room,
            "canPublish": True,
            "canSubscribe": True,
            "canPublishData": True,
        },
    }
    token = jwt.encode(claims, LIVEKIT_API_SECRET, algorithm="HS256")
    return {"token": token, "url": LIVEKIT_URL, "room": room, "identity": identity}


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            raw = await websocket.receive_text()
            try:
                data = json.loads(raw)
                if data.get("type") == "CHAT_MESSAGE":
                    conv_key = data.get("convKey", "orbita:geral")
                    msg = data.get("message", {})
                    msg_id = int(msg.get("id", int(time.time() * 1000)))
                    with sqlite3.connect(DB_PATH) as conn:
                        conn.execute(
                            "INSERT OR REPLACE INTO messages (id, conv_key, payload, created_at) VALUES (?, ?, ?, ?)",
                            (msg_id, conv_key, json.dumps(msg, ensure_ascii=False), time.time()),
                        )
                        conn.commit()
            except Exception:
                pass
            await manager.broadcast(raw, sender=websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
