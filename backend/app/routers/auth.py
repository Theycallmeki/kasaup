from fastapi import APIRouter, Depends, HTTPException, Response, Request, status
from sqlalchemy.orm import Session
from jose import jwt, JWTError

from app.db import get_db
from app.models.users import User
from app.schemas.auth import LoginRequest
from app.schemas.users import UserOut
from app.core.security import (
    verify_password,
    create_access_token,
    create_refresh_token,
    SECRET_KEY,
    ALGORITHM
)
from app.core.dependencies import get_current_user

router = APIRouter()


@router.post("/login/")
def login(data: LoginRequest, response: Response, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()

    if not user or not verify_password(data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    if user.role == "provider" and not user.is_approved:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Your provider account is pending admin approval."
        )

    access_token = create_access_token({"user_id": user.id})
    refresh_token = create_refresh_token({"user_id": user.id})

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        samesite="lax",
        secure=False
    )

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        samesite="lax",
        secure=False
    )

    return {"message": "Login successful"}


@router.post("/refresh/")
def refresh_token(request: Request, response: Response, db: Session = Depends(get_db)):
    refresh_token = request.cookies.get("refresh_token")

    if not refresh_token:
        raise HTTPException(status_code=401, detail="Refresh token missing")

    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])

        if payload.get("type") != "refresh":
            raise HTTPException(status_code=401, detail="Invalid token")

        user_id = payload.get("user_id")

        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    new_access_token = create_access_token({"user_id": user_id})

    response.set_cookie(
        key="access_token",
        value=new_access_token,
        httponly=True,
        samesite="lax",
        secure=False
    )

    return {"message": "Access token refreshed"}


@router.post("/logout/")
def logout(response: Response):
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")

    return {"message": "Logged out"}


@router.get("/me/", response_model=UserOut, dependencies=[Depends(get_current_user)])
def get_me(current_user: User = Depends(get_current_user)):
    return current_user