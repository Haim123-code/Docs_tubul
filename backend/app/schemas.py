from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    email: EmailStr
    name: str
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    name: str
    class Config:
        from_attributes = True

class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"

class DocumentCreate(BaseModel):
    title: str = "Untitled"
    content_json: str = "{}"

class DocumentUpdate(BaseModel):
    title: Optional[str] = None
    content_json: Optional[str] = None

class DocumentOut(BaseModel):
    id: int
    title: str
    content_json: str
    owner_id: int
    class Config:
        from_attributes = True
