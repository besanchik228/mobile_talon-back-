from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import Optional
from database import get_db
from models import User, UserRole
import os

#hash_password - хеширует пароль
#verify_password - проверяет пароль
#create_token - создает токен
#get_user_login - получает пользователя по логину
#get_cur_user - получает текущего пользователя
#require_teacher - проверяет, что пользователь имеет роль учителя
#require_canteen - проверяет, что пользователь имеет роль столовой

context = CryptContext(schemes=["bcrypt"], deprecated="auto")
auth_scheme = OAuth2PasswordBearer(tokenUrl="/api/token")


def hash_password(password: str) -> str:
    return context.hash(password)

def verify_password(password, hashed_password) -> bool:
    return context.verify(password, hashed_password)

def create_token(sub: str, role: UserRole) -> str:
    exp = datetime.now() + timedelta(minutes=os.getenv("access_token"))
    to = {"sub" : sub, "exp" : exp, "role" : role.value}
    enc = jwt.encode(to, os.getenv("secret_key"), algorithm="algoritm")
    return enc

def get_user_login(db: Session, login : str) -> Optional[User]:
    return db.query(User).filter(User.username == login).first()

async def get_cur_user(db: Session, token: str = Depends(auth_scheme)):
    try:
        payload = jwt.decode(token, os.getenv("secret_key"), algorithms=os.getenv("algoritm"))
        login: str = payload.get("sub")
        role: str = payload.get("role")
        if login is None or role is None:
            raise HTTPException(status_code=401, detail="Not authenticated")
    except JWTError:
        raise HTTPException(status_code=401, detail="Not authenticated")
    user = get_user_login(db, login)
    if user is None:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return user

async def require_teacher(user: User = Depends(get_cur_user)) -> User:
    if user.role != UserRole.teacher:
        raise HTTPException(status_code=403, detail="Teacher role required")
    return user


async def require_canteen(user: User = Depends(get_cur_user)) -> User:
    if user.role != UserRole.canteen:
        raise HTTPException(status_code=403, detail="Canteen role required")
    return user