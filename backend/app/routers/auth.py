from fastapi import APIRouter, Depends, HTTPException, Response, Request, status
from fastapi.responses import RedirectResponse
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
from app.services.google_oauth import get_google_auth_url, get_google_user
from app.services.github_oauth import get_github_auth_url, get_github_user
from app.core.config import settings

router = APIRouter()


@router.get("/google")
def google_login(role: str = "customer"):
    return RedirectResponse(get_google_auth_url(role))


@router.get("/google/callback")
async def google_callback(code: str, state: str = "customer", db: Session = Depends(get_db)):
    try:
        user_data = await get_google_user(code)
    except Exception as e:
        return RedirectResponse(url=f"{settings.FRONTEND_URL}/login?error=google_auth_failed")

    email = user_data["email"]
    full_name = user_data.get("name")
    profile_image = user_data.get("picture")

    user = db.query(User).filter(User.email == email).first()

    if not user:
        user = User(
            email=email,
            full_name=full_name,
            profile_image=profile_image,
            role=state,
            is_approved=True if state == "customer" else False
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    target_path = "/"
    if user.role == "customer":
        target_path = "/services"
    elif user.role == "provider":
        if not user.provided_shop:
            target_path = "/provider/create-profile"
        else:
            target_path = "/provider/dashboard"
    elif user.role == "admin":
        target_path = "/admin/dashboard"

    if user.role == "provider" and not user.is_approved:
        return RedirectResponse(url=f"{settings.FRONTEND_URL}/login?error=pending_approval")

    access_token = create_access_token({"user_id": user.id})
    refresh_token = create_refresh_token({"user_id": user.id})

    response = RedirectResponse(url=f"{settings.FRONTEND_URL}{target_path}")

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        samesite="none",
        secure=True
    )

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        samesite="none",
        secure=True
    )

    return response


@router.get("/github")
def github_login(role: str = "customer"):
    return RedirectResponse(get_github_auth_url(role))


@router.get("/github/callback")
async def github_callback(code: str, state: str = "customer", db: Session = Depends(get_db)):
    try:
        user_data = await get_github_user(code)
    except Exception as e:
        return RedirectResponse(url=f"{settings.FRONTEND_URL}/login?error=github_auth_failed")

    email = user_data["email"]
    full_name = user_data.get("name")
    profile_image = user_data.get("picture")

    user = db.query(User).filter(User.email == email).first()

    if not user:
        user = User(
            email=email,
            full_name=full_name,
            profile_image=profile_image,
            role=state,
            is_approved=True if state == "customer" else False
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    target_path = "/"
    if user.role == "customer":
        target_path = "/services"
    elif user.role == "provider":
        if not user.provided_shop:
            target_path = "/provider/create-profile"
        else:
            target_path = "/provider/dashboard"
    elif user.role == "admin":
        target_path = "/admin/dashboard"

    if user.role == "provider" and not user.is_approved:
        return RedirectResponse(url=f"{settings.FRONTEND_URL}/login?error=pending_approval")

    access_token = create_access_token({"user_id": user.id})
    refresh_token = create_refresh_token({"user_id": user.id})

    response = RedirectResponse(url=f"{settings.FRONTEND_URL}{target_path}")

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        samesite="none",
        secure=True
    )

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        samesite="none",
        secure=True
    )

    return response


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
        samesite="none",
        secure=True
    )

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        samesite="none",
        secure=True
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
        samesite="none",
        secure=True
    )

    return {"message": "Access token refreshed"}


@router.post("/logout/")
def logout(response: Response):
    response.delete_cookie(key="access_token", samesite="none", secure=True)
    response.delete_cookie(key="refresh_token", samesite="none", secure=True)

    return {"message": "Logged out"}


@router.get("/me/", response_model=UserOut, dependencies=[Depends(get_current_user)])
def get_me(current_user: User = Depends(get_current_user)):
    current_user.has_profile = True if current_user.provided_shop else False
    return current_user