from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from auth import get_current_user, get_password_hash
from database import get_db
from models import User, UserRole
from schemas import UserPublic, ProfileUpdate

router = APIRouter(prefix="/profile", tags=["profile"])


@router.get("/me", response_model=UserPublic)
def get_me(user: User = Depends(get_current_user)):
    return user


@router.put("/me", response_model=UserPublic)
def update_me(
    payload: ProfileUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    if payload.educational_institution is not None:
        user.educational_institution = payload.educational_institution

    if payload.password:
        user.hashed_password = get_password_hash(payload.password)

    if user.role == UserRole.teacher:
        if payload.class_name is not None:
            user.class_name = payload.class_name
        if payload.canteen_id is not None:
            canteen = db.query(User).filter(User.id == payload.canteen_id, User.role == UserRole.canteen).first()
            if not canteen:
                raise HTTPException(status_code=404, detail="Canteen not found")
            user.canteen_id = payload.canteen_id

    db.add(user)
    db.commit()
    db.refresh(user)
    return user
