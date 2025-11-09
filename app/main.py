from fastapi import FastAPI
from app.api.routs import products
from app.api.routs import auth 
from app.api.routs import order
from app.api.routs import users

app = FastAPI(
    title="Marketplace Agro API",
    version="0.1.0"
)


app.include_router(
    auth.router, 
    prefix="/auth", 
    tags=["Autenticação"]
)

app.include_router(
    products.router, 
    prefix="/api/v1", 
    tags=["Produtos"]
)

app.include_router(
    order.router, 
    prefix="/api/v1", 
    tags=["Pedidos"]
)

app.include_router(
    users.router, 
    prefix="/api/v1", 
    tags=["Admin (Utilizadores)"]
)
