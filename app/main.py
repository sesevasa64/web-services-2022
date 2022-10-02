from fastapi import FastAPI
from app.routers import router
from app.auth.routers import router as auth_router
from app.shop.routers import router as shop_router


app = FastAPI(
    title="BaseApp",
    description=("BaseApp"),
    version="0.0.1",
    docs_url="/docs",
    redoc_url="/docs/redoc"
)

app.include_router(router)
app.include_router(auth_router)
app.include_router(shop_router)
