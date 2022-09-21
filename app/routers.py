from typing import Optional
from fastapi import APIRouter
from app.contracts import User


router = APIRouter()


@router.get("/")
async def read_root():
    return {"Hello": "World"}

@router.get("/items/{item_id}")
async def read_item(item_id: int):
    """Get item by item_id"""
    return {"item_id": item_id}

@router.get("/users/")
async def read_user(user_id: str, q: Optional[str] = None):
    """Get user by user_id"""
    if q:
        return {"item_id": user_id, "q": q}
    return {"item_id": user_id}

@router.post("/users/")
async def create_user(user: User):
    """Post new user"""
    return user
