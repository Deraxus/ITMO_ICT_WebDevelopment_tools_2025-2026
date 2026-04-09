from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.security import (
    create_access_token,
    hash_password,
    verify_password
)
from app.crud import get_user_by_email, update_user_password
from app.db import get_db
from app.models.user import User
from app.schemas.auth import ChangePasswordRequest, Token
from app.schemas.user import UserRead


router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login", response_model=Token)
def login_endpoint(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = get_user_by_email(db, form_data.username)

    if user is None or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )

    access_token = create_access_token(data={"sub": str(user.id)})

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


@router.get("/me", response_model=UserRead)
def get_current_user_endpoint(current_user: User = Depends(get_current_user)):
    return current_user


@router.post("/change-password")
def change_password_endpoint(
    password_data: ChangePasswordRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not verify_password(password_data.old_password, current_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Old password is incorrect"
        )

    new_hashed_password = hash_password(password_data.new_password)
    update_user_password(db, current_user, new_hashed_password)

    return {"message": "Password changed successfully"}