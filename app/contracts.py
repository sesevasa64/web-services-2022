from typing import List
from pydantic import BaseModel


class User(BaseModel):
    """Contract for User."""
    uid: int
    login: str
    password: str
    money: int = 0

class UserRegistration(BaseModel):
    login: str
    password: str

class Product(BaseModel):
    uid: int
    name: str
    description: str = ""
    type: str
    cost: int

class ProductRegistration(BaseModel):
    name: str
    description: str = ""
    type: str
    cost: int

class UserOrder(BaseModel):
    uuid: int
    puids: List[int]
