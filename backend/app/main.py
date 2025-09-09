from fastapi import FastAPI, Depends, HTTPException, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from .database import Base, engine, get_db
from . import models, crud
from .schemas import UserCreate, UserOut, TokenOut, DocumentCreate, DocumentUpdate, DocumentOut
from .auth import create_access_token, verify_password, get_current_user
from fastapi.middleware.cors import CORSMiddleware
from .realtime import hub

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Collaborative Docs – MVP")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/auth/register", response_model=UserOut)
def register(user: UserCreate, db: Session = Depends(get_db)):
    if crud.get_user_by_email(db, user.email):
        raise HTTPException(400, "Email already registered")
    u = crud.create_user(db, user)
    return u

@app.post("/auth/login", response_model=TokenOut)
def login(user: UserCreate, db: Session = Depends(get_db)):
    u = crud.get_user_by_email(db, user.email)
    if not u or not verify_password(user.password, u.password_hash):
        raise HTTPException(401, "Invalid credentials")
    token = create_access_token(u.email)
    return {"access_token": token, "token_type": "bearer"}

@app.post("/documents", response_model=DocumentOut)
def create_document(doc: DocumentCreate, current=Depends(get_current_user), db: Session = Depends(get_db)):
    return crud.create_document(db, current.id, doc)

@app.get("/documents", response_model=list[DocumentOut])
def list_my_documents(current=Depends(get_current_user), db: Session = Depends(get_db)):
    return crud.list_documents(db, current.id)

@app.get("/documents/{doc_id}", response_model=DocumentOut)
def get_document(doc_id: int, current=Depends(get_current_user), db: Session = Depends(get_db)):
    d = crud.get_document(db, doc_id)
    if not d or d.owner_id != current.id:
        raise HTTPException(404, "Document not found")
    return d

@app.put("/documents/{doc_id}", response_model=DocumentOut)
def update_document(doc_id: int, doc: DocumentUpdate, current=Depends(get_current_user), db: Session = Depends(get_db)):
    d = crud.get_document(db, doc_id)
    if not d or d.owner_id != current.id:
        raise HTTPException(404, "Document not found")
    updated = crud.update_document(db, doc_id, doc)
    return updated

@app.delete("/documents/{doc_id}")
def delete_document(doc_id: int, current=Depends(get_current_user), db: Session = Depends(get_db)):
    d = crud.get_document(db, doc_id)
    if not d or d.owner_id != current.id:
        raise HTTPException(404, "Document not found")
    ok = crud.delete_document(db, doc_id)
    return {"ok": ok}

# WebSocket לשיתופיות בסיסית (שידור עדכונים בין קליינטים)
@app.websocket("/ws/docs/{doc_id}")
async def ws_docs(websocket: WebSocket, doc_id: str):
    await hub.connect(doc_id, websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await hub.broadcast(doc_id, data, sender=websocket)
    except WebSocketDisconnect:
        hub.disconnect(doc_id, websocket)
