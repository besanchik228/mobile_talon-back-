from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from auth import create_access_token, verify_password, get_password_hash, get_user_by_login
from database import get_db
from models import User, UserRole
from schemas import (
    LoginRequest, TokenResponse,
    RegisterCanteenRequest, RegisterTeacherRequest,
    UserPublic
)

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register/canteen", response_model=UserPublic)
def register_canteen(payload: RegisterCanteenRequest, db: Session = Depends(get_db)):
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


@router.post("/register/teacher", response_model=UserPublic)
def register_teacher(payload: RegisterTeacherRequest, db: Session = Depends(get_db)):
    if get_user_by_login(db, payload.login):
        raise HTTPException(status_code=400, detail="Login already exists")

    # Проверка привязки к существующей столовой
    canteen = db.query(User).filter(User.id == payload.canteen_id, User.role == UserRole.canteen).first()
    if not canteen:
        raise HTTPException(status_code=404, detail="Canteen not found")

    user = User(
        login=payload.login,
        hashed_password=get_password_hash(payload.password),
        educational_institution=payload.educational_institution,
        role=UserRole.teacher,
        class_name=payload.class_name.strip(),
        canteen_id=payload.canteen_id
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = get_user_by_login(db, payload.login)
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid login or password")

    token = create_access_token(subject=user.login, role=user.role)
    return TokenResponse(access_token=token, role=user.role)
