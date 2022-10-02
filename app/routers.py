from fastapi import APIRouter
from app.database import *
from app.contracts import *


router = APIRouter()
database = Database()

database.add_product(ProductRegistration(
    name="Пеперони", type="Пицца", cost=320
))
database.add_product(ProductRegistration(
    name="Маргарита", type="Пицца", cost=250
))

@router.get("/")
async def read_root():
    return {"Hello": "World"}
