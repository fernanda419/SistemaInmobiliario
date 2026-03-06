from fastapi import APIRouter
from app.controllers.auth_controller import login, register

router = APIRouter(prefix="/auth", tags=["Auth"])

router.post("/register")(register)
router.post("/login")(login)