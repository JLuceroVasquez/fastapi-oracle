from fastapi import FastAPI
from app.routers import todos, users, login

# 1. INICIALIZACIÓN DE LA APLICACIÓN
# Creamos la instancia principal de FastAPI.
app = FastAPI()

app.include_router(router=todos.router, tags=["Todos"], prefix="/todos")
app.include_router(router=users.router, tags=["Users"], prefix="/users")
app.include_router(router=login.router, tags=["Login"], prefix="/login")

