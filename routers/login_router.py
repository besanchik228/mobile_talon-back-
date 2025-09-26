from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

# Импортируем вспомогательные функции для работы с аутентификацией
from auth import create_access_token, verify_password, get_user_by_login
from database import get_db
from schemas import (
    LoginRequest, TokenResponse
)

router = APIRouter(prefix="/login", tags=["login"])

@router.post("/", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    """
    Авторизация пользователя.
    - Проверяем, что пользователь существует.
    - Сверяем пароль с хэшированным.
    - Если всё верно — создаём JWT-токен с ролью пользователя.
    - Возвращаем токен и роль.
    """
    user = get_user_by_login(db, payload.login)
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid login or password")

    token = create_access_token(subject=user.login, role=user.role)
    return TokenResponse(access_token=token, role=user.role)