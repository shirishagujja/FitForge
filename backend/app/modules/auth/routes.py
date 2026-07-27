"""Auth HTTP routes."""

from __future__ import annotations

from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_current_user, get_db
from app.modules.auth import service as auth_service
from app.modules.auth.models import User
from app.modules.auth.schemas import (
    ForgotPasswordRequest,
    LoginRequest,
    LogoutRequest,
    RefreshRequest,
    RegisterRequest,
    ResetPasswordRequest,
)
from app.modules.profile import service as profile_service

router = APIRouter(prefix="/auth", tags=["auth"])


def _client_meta(request: Request) -> tuple[str | None, str | None]:
    user_agent = request.headers.get("user-agent")
    ip_address = request.client.host if request.client else None
    return user_agent, ip_address


@router.post("/register", status_code=201)
async def register(
    payload: RegisterRequest,
    db: AsyncSession = Depends(get_db),
) -> dict:
    user = await auth_service.register_user(db, payload)
    return {
        "data": auth_service.to_user_response(user),
        "message": (
            "Registration successful. Please check your email to verify your account."
        ),
    }


@router.post("/login")
async def login(
    payload: LoginRequest,
    request: Request,
    db: AsyncSession = Depends(get_db),
) -> dict:
    user_agent, ip_address = _client_meta(request)
    tokens = await auth_service.authenticate_user(
        db,
        payload,
        user_agent=user_agent,
        ip_address=ip_address,
    )
    return {"data": tokens}


@router.post("/refresh")
async def refresh(
    payload: RefreshRequest,
    request: Request,
    db: AsyncSession = Depends(get_db),
) -> dict:
    user_agent, ip_address = _client_meta(request)
    tokens = await auth_service.refresh_tokens(
        db,
        payload.refresh_token,
        user_agent=user_agent,
        ip_address=ip_address,
    )
    return {"data": tokens}


@router.post("/logout")
async def logout(
    payload: LogoutRequest,
    db: AsyncSession = Depends(get_db),
) -> dict:
    await auth_service.logout(db, payload.refresh_token)
    return {"data": None, "message": "Logged out successfully"}


@router.get("/verify-email")
async def verify_email(
    token: str = Query(min_length=1),
    db: AsyncSession = Depends(get_db),
) -> dict:
    user = await auth_service.verify_email(db, token)
    return {
        "data": {"email_verified": user.email_verified},
        "message": "Email verified successfully",
    }


@router.post("/resend-verification")
async def resend_verification(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> dict:
    await auth_service.resend_verification_email(db, user)
    return {
        "data": None,
        "message": "If your email is unverified, a new verification link has been sent.",
    }


@router.post("/forgot-password")
async def forgot_password(
    payload: ForgotPasswordRequest,
    db: AsyncSession = Depends(get_db),
) -> dict:
    await auth_service.request_password_reset(db, payload.email)
    return {
        "data": None,
        "message": "If an account exists with this email, a reset link has been sent.",
    }


@router.post("/reset-password")
async def reset_password(
    payload: ResetPasswordRequest,
    db: AsyncSession = Depends(get_db),
) -> dict:
    await auth_service.reset_password(db, payload)
    return {
        "data": None,
        "message": "Password reset successfully",
    }


@router.get("/me", response_model=None)
async def me(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> dict:
    profile_exists = await profile_service.has_profile(db, user)
    body = auth_service.to_me_response(user, has_profile=profile_exists)
    return {"data": body}
