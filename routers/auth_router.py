from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

# Импортируем вспомогательные функции для работы с аутентификацией
from auth import get_password_hash, get_user_by_login
from database import get_db
from models import User, UserRole
from schemas import (
    RegisterCanteenRequest, RegisterTeacherRequest,
    UserPublic
)

# Создаём роутер для всех эндпоинтов, связанных с аутентификацией
router = APIRouter(prefix="/register", tags=["register"])


@router.post("/canteen", response_model=UserPublic)
def register_canteen(payload: RegisterCanteenRequest, db: Session = Depends(get_db)):
    """
    Регистрация пользователя с ролью 'canteen' (столовая).
    - Проверяем, что логин ещё не занят.
    - Хэшируем пароль.
    - Создаём нового пользователя с ролью 'canteen'.
    - Сохраняем в БД и возвращаем публичные данные пользователя.
    """
    if get_user_by_login(db, payload.login):
        raise HTTPException(status_code=400, detail="Login already exists")

    user = User(
        login=payload.login,
        hashed_password=get_password_hash(payload.password),
        educational_institution=payload.educational_institution,
        role=UserRole.canteen
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.post("/teacher", response_model=UserPublic)
def register_teacher(payload: RegisterTeacherRequest, db: Session = Depends(get_db)):
    """
    Регистрация пользователя с ролью 'teacher' (учитель).
    - Проверяем, что логин ещё не занят.
    - Проверяем, что указанная столовая (canteen_id) существует.
    - Создаём нового пользователя с ролью 'teacher', привязанного к столовой.
    - Сохраняем в БД и возвращаем публичные данные пользователя.
    """
    if get_user_by_login(db, payload.login):
        raise HTTPException(status_code=400, detail="Login already exists")

    # Проверка, что столовая существует и имеет правильную роль
    canteen = db.query(User).filter(User.id == payload.canteen_id, User.role == UserRole.canteen).first()
    if not canteen:
        raise HTTPException(status_code=404, detail="Canteen not found")

    user = User(
        login=payload.login,
        hashed_password=get_password_hash(payload.password),
        educational_institution=payload.educational_institution,
        role=UserRole.teacher,
        class_name=payload.class_name.strip(),  # убираем лишние пробелы
        canteen_id=payload.canteen_id
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


# @router.post("/login", response_model=TokenResponse)
# def login(payload: LoginRequest, db: Session = Depends(get_db)):
#     """
#     Авторизация пользователя.
#     - Проверяем, что пользователь существует.
#     - Сверяем пароль с хэшированным.
#     - Если всё верно — создаём JWT-токен с ролью пользователя.
#     - Возвращаем токен и роль.
#     """
#     user = get_user_by_login(db, payload.login)
#     if not user or not verify_password(payload.password, user.hashed_password):
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid login or password")
#
#     token = create_access_token(subject=user.login, role=user.role)
#     return TokenResponse(access_token=token, role=user.role)
