from fastapi import FastAPI
from app.routers import todos, users, login
from fastapi.middleware.cors import CORSMiddleware

# 1. INICIALIZACIÓN DE LA APLICACIÓN
# Creamos la instancia principal de FastAPI.
app = FastAPI()

#Configuramos CORS para permitir acceso desde otros servidores para probar la API.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(router=todos.router, tags=["Todos"], prefix="/todos")
app.include_router(router=users.router, tags=["Users"], prefix="/users")
app.include_router(router=login.router, tags=["Login"], prefix="/login")

