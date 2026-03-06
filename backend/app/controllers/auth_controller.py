from fastapi import HTTPException
from app.services.auth_service import authenticate_user, create_user

async def register(user: dict):

    print("Datos recibidos:", user)

    return create_user(user)

async def login(data: dict):
    user = authenticate_user(data["email"], data["password"])

    if not user:
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")

    return user