from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from schemas.auth import SignupRequest, LoginRequest, TokenResponse, UserOut
from services.auth_service import AuthService, get_current_user
from models.user import User

router = APIRouter()


@router.post("/signup", response_model=TokenResponse, status_code=201)
async def signup(body: SignupRequest, db: AsyncSession = Depends(get_db)):
    service = AuthService(db)
    token, user = await service.signup(body.email, body.password)
    return {"access_token": token, "user": user}


@router.post("/login", response_model=TokenResponse)
async def login(body: LoginRequest, db: AsyncSession = Depends(get_db)):
    service = AuthService(db)
    token, user = await service.login(body.email, body.password)
    return {"access_token": token, "user": user}


@router.get("/me", response_model=UserOut)
async def me(current_user: User = Depends(get_current_user)):
    return current_user