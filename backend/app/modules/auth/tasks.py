"""Celery tasks for auth-related emails."""

from __future__ import annotations

import logging

from app.core.email import (
    build_password_reset_email,
    build_verification_email,
    send_email,
)
from celery_app import celery_app

logger = logging.getLogger(__name__)


@celery_app.task(name="auth.send_verification_email", queue="email")
def send_verification_email(to_email: str, raw_token: str) -> None:
    payload = build_verification_email(to_email, raw_token)
    send_email(payload)
    logger.info("verification_email_queued to=%s", to_email)


@celery_app.task(name="auth.send_password_reset_email", queue="email")
def send_password_reset_email(to_email: str, raw_token: str) -> None:
    payload = build_password_reset_email(to_email, raw_token)
    send_email(payload)
    logger.info("password_reset_email_queued to=%s", to_email)
