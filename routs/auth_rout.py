from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from auth import hash_password, verify_password, get_user_login, create_token
from database import get_db
from models import User, UserRole
from schemas import (
    RegisterTeacherRequest, RegisterCanteenRequest,
    LoginRequest, TokenResponse, UserPublic
)


router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login", response_model=UserPublic)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = get_user_login(db, payload.login)
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    token = create_token(subject=user.login, role=user.role)
    return TokenResponse(access_token=token, role=user.role)


@router.post("/register/canteen", response_model=UserPublic)
def register_canteen(payload: RegisterCanteenRequest, db: Session = Depends(get_db)):
    if get_user_login(db, payload.login):
        raise HTTPException(status_code=400, detail="Login already exists")
    user = User(
        login=payload.login,
        hashed_password=hash_password(payload.password),
        role=UserRole.canteen,
        edu=payload.edu
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.post("register/teacher", response_model=UserPublic)
def register_teacher(payload: RegisterTeacherRequest, db: Session = Depends(get_db)):
    if get_user_login(db, payload.login):
        raise HTTPException(status_code=400, detail="Login already exists")
    user = User(
        login=payload.login,
        hashed_password=hash_password(payload.password),
        role=UserRole.teacher,
        edu=payload.edu,
        class_name=payload.class_name,
        canteen_id=payload.canteen_id
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user