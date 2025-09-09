from fastapi import WebSocket, WebSocketDisconnect
from typing import Dict, Set

# MVP Broadcaster: לא CRDT אמיתי — רק שידור בין מחוברים לאותו מסמך
class Hub:
    def __init__(self):
        self.rooms: Dict[str, Set[WebSocket]] = {}

    async def connect(self, doc_id: str, ws: WebSocket):
        await ws.accept()
        self.rooms.setdefault(doc_id, set()).add(ws)

    def disconnect(self, doc_id: str, ws: WebSocket):
        if doc_id in self.rooms and ws in self.rooms[doc_id]:
            self.rooms[doc_id].remove(ws)
            if not self.rooms[doc_id]:
                del self.rooms[doc_id]

    async def broadcast(self, doc_id: str, data: str, sender: WebSocket):
        for ws in list(self.rooms.get(doc_id, [])):
            if ws is not sender:
                await ws.send_text(data)

hub = Hub()
