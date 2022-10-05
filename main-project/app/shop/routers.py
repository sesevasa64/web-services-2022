from app.contracts import UserOrder
from app.database import Database, UserNotExistError, ProductNotExistError
from fastapi import APIRouter, HTTPException

router = APIRouter()
database = Database()

@router.get("/product")
async def product(puid: int):
    try:
        return database.get_product(puid)
    except ProductNotExistError:
        raise HTTPException(status_code=404, detail=f"Product with id '{puid}' not exist in db.")

@router.get("/products")
async def products():
    return database.get_products()

@router.post("/order")
async def order(user_order: UserOrder):
    products = []
    try:
        user = database.get_user(user_order.uuid)
    except UserNotExistError:
        raise HTTPException(status_code=404, detail=f"User with id '{user_order.uuid}' not exist in db.")
    for puid in user_order.puids:
        try:
            products.append(database.get_product(puid))
        except ProductNotExistError:
            raise HTTPException(status_code=404, detail=f"Product with id '{puid}' not exist in db.")
    products_cost = sum([p.cost for p in products])
    if user.money < products_cost:
       pass
    user.money -= products_cost
    return products
