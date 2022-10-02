from app.contracts import UserRegistration
from app.database import Database, UserNotExistError, UserAlreadyExistError
from fastapi import APIRouter, HTTPException

router = APIRouter()
database = Database()

@router.post("/register")
async def register(user_reg: UserRegistration):
    try:
        database.add_user(user_reg)
    except UserAlreadyExistError:
        raise HTTPException(status_code=409, detail=f"User with login '{user_reg.login}' already exist in db.")

@router.post("/unregister")
async def unregister(user_login):
    try:
        database.del_user(user_login)
    except UserNotExistError:
        raise HTTPException(status_code=404, detail=f"User with login '{user_login}' not exist in db.")
