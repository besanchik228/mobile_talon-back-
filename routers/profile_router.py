from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from auth import get_current_user, get_password_hash
from database import get_db
from models import User, UserRole
from schemas import UserPublic, ProfileUpdate

# Роутер для работы с профилем пользователя
router = APIRouter(prefix="/profile", tags=["profile"])


@router.get("/me", response_model=UserPublic)
def get_me(user: User = Depends(get_current_user)):
    """
    Эндпоинт для получения информации о текущем пользователе.
    - Использует Depends(get_current_user), чтобы извлечь пользователя из токена.
    - Возвращает публичные данные пользователя (схема UserPublic).
    """
    return user


@router.put("/me", response_model=UserPublic)
def update_me(
    payload: ProfileUpdate,              # Данные для обновления профиля
    db: Session = Depends(get_db),       # Сессия базы данных
    user: User = Depends(get_current_user),  # Текущий пользователь
):
    """
    Эндпоинт для обновления профиля текущего пользователя.
    Доступные изменения:
    - educational_institution (учебное заведение)
    - password (с автоматическим хэшированием)
    - class_name и canteen_id (только для учителей)
    """

    # Обновляем учебное заведение, если передано
    if payload.educational_institution is not None:
        user.educational_institution = payload.educational_institution

    # Если передан новый пароль — хэшируем и сохраняем
    if payload.password:
        user.hashed_password = get_password_hash(payload.password)

    # Дополнительные поля доступны только для учителей
    if user.role == UserRole.teacher:
        # Обновляем название класса
        if payload.class_name is not None:
            user.class_name = payload.class_name
        # Обновляем привязку к столовой
        if payload.canteen_id is not None:
            canteen = db.query(User).filter(
                User.id == payload.canteen_id,
                User.role == UserRole.canteen
            ).first()
            if not canteen:
                # Если указанной столовой нет — ошибка
                raise HTTPException(status_code=404, detail="Canteen not found")
            user.canteen_id = payload.canteen_id

    # Сохраняем изменения в базе
    db.add(user)
    db.commit()
    db.refresh(user)

    # Возвращаем обновлённые публичные данные
    return user
