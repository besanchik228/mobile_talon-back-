from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from environ_init import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_TIME
from database import get_db
from models import User, UserRole


# Контекст для работы с паролями (bcrypt — алгоритм хэширования)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Настройка схемы OAuth2: токен будет передаваться в заголовке Authorization: Bearer <token>
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_password_hash(password: str) -> str:
    """
    Хэширует пароль с использованием bcrypt.
    Используется при регистрации и смене пароля.
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Проверяет соответствие введённого пароля и хэша из базы.
    Возвращает True, если пароль верный.
    """
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(subject: str, role: UserRole, expires_delta: Optional[timedelta] = None) -> str:
    """
    Создаёт JWT-токен для пользователя.
    - subject: логин пользователя
    - role: роль пользователя (teacher/canteen)
    - expires_delta: время жизни токена (по умолчанию берётся из ACCESS_TOKEN_TIME)
    """
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_TIME))
    to_encode = {"sub": subject, "role": role.value, "exp": expire}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_user_by_login(db: Session, login: str) -> Optional[User]:
    """
    Возвращает пользователя по логину или None, если не найден.
    """
    return db.query(User).filter(User.login == login).first()


async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    """
    Декодирует JWT-токен и возвращает текущего пользователя.
    - Проверяет подпись токена и срок действия.
    - Извлекает логин и роль.
    - Находит пользователя в базе.
    - Если что-то не так — выбрасывает 401 Unauthorized.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        login: str = payload.get("sub")
        role: str = payload.get("role")
        if login is None or role is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = get_user_by_login(db, login)
    if user is None:
        raise credentials_exception
    return user


async def require_teacher(user: User = Depends(get_current_user)) -> User:
    """
    Депенденси для эндпоинтов, доступных только учителям.
    Если роль не teacher — возвращает 403 Forbidden.
    """
    if user.role != UserRole.teacher:
        raise HTTPException(status_code=403, detail="Teacher role required")
    return user


async def require_canteen(user: User = Depends(get_current_user)) -> User:
    """
    Депенденси для эндпоинтов, доступных только столовым.
    Если роль не canteen — возвращает 403 Forbidden.
    """
    if user.role != UserRole.canteen:
        raise HTTPException(status_code=403, detail="Canteen role required")
    return user
