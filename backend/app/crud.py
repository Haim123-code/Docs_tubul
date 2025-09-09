from sqlalchemy.orm import Session
from . import models
from .schemas import DocumentCreate, DocumentUpdate, UserCreate
from .auth import hash_password

def create_user(db: Session, user_in: UserCreate) -> models.User:
    user = models.User(email=user_in.email, name=user_in.name, password_hash=hash_password(user_in.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_document(db: Session, owner_id: int, doc_in: DocumentCreate) -> models.Document:
    doc = models.Document(title=doc_in.title, content_json=doc_in.content_json, owner_id=owner_id)
    db.add(doc)
    db.commit()
    db.refresh(doc)
    return doc

def list_documents(db: Session, owner_id: int):
    return db.query(models.Document).filter(models.Document.owner_id == owner_id).order_by(models.Document.updated_at.desc()).all()

def get_document(db: Session, doc_id: int):
    return db.query(models.Document).filter(models.Document.id == doc_id).first()

def update_document(db: Session, doc_id: int, doc_in: DocumentUpdate):
    doc = get_document(db, doc_id)
    if not doc:
        return None
    if doc_in.title is not None:
        doc.title = doc_in.title
    if doc_in.content_json is not None:
        doc.content_json = doc_in.content_json
    from datetime import datetime
    doc.updated_at = datetime.utcnow()
    db.add(doc)
    db.commit()
    db.refresh(doc)
    return doc

def delete_document(db: Session, doc_id: int) -> bool:
    doc = get_document(db, doc_id)
    if not doc:
        return False
    db.delete(doc)
    db.commit()
    return True
