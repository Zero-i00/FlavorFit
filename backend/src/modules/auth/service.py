from datetime import timedelta
from typing import Any, Optional

from fastapi import Request, status, Response, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from database.models.user import UserModel
from modules.user.service import user_service
from modules.user.schema import UserInput

from modules.auth.strategies.jwt_token import jwt_strategy
from modules.auth.schema import AuthInput, AuthTokenEnum

from config.settings import settings, auth_settings, IS_DEBUG
from utils.normalize import normalize_email


async def register(session: AsyncSession, data: AuthInput) -> UserModel:
    data.email = normalize_email(data.email)

    existing = await user_service.get_by_email(session, data.email)
    if existing:
        raise user_service.already_exists_exception

    user = await user_service.create(session, UserInput(
        email=data.email,
        password=data.password,
    ))

    return user


class AuthService:
    def __init__(self) -> None:
        self.invalid_token_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid jwt token",
        )

        self.invalid_credentials_exception = HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid login or password",
        )

    async def login(self, session: AsyncSession, data: AuthInput) -> UserModel:
        data.email = normalize_email(data.email)

        user = await user_service.get_by_email(session, data.email)
        if user is None:
            raise self.invalid_credentials_exception

        if not user_service.validate_password(data.password, user.password):
            raise self.invalid_credentials_exception

        return user

    async def refresh_token(self, session: AsyncSession, request: Request) -> UserModel:
        payload = self.get_token_payload(
            request=request,
            token_type=AuthTokenEnum.REFRESH_TOKEN,
        )

        user_id = payload.get('user_id', None)
        if user_id is None:
            raise self.invalid_token_exception

        user = await user_service.retrieve(session, int(user_id))
        return user

    async def logout(self, session: AsyncSession, refresh_token: str) -> None:
        # TODO jwt refresh token black list
        return

    def get_token_payload(self, request: Request, token_type: AuthTokenEnum) -> dict[str, Any]:
        match token_type:
            case AuthTokenEnum.ACCESS_TOKEN:
                auth_header: Optional[str] = request.headers.get("Authorization")
                if not auth_header:
                    raise self.invalid_token_exception

                schema, _, token = auth_header.partition(" ")
                if schema.lower() != 'bearer':
                    raise self.invalid_token_exception

            case AuthTokenEnum.REFRESH_TOKEN:
                token = request.cookies.get(token_type.value, None)
                if token is None:
                    raise self.invalid_token_exception

            case _:
                raise self.invalid_token_exception

        payload = jwt_strategy.decode_jwt(token)
        if payload is None:
            raise self.invalid_token_exception

        return payload

    @staticmethod
    def create_access_token(user: UserModel) -> str:
        payload = {
            'sub': user.email,
            'role': user.role.value,
            'user_id': user.id,
            'email': user.email,
            'type': AuthTokenEnum.ACCESS_TOKEN.value,
        }
        return jwt_strategy.encode_jwt(payload)

    @staticmethod
    def create_refresh_token(user: UserModel) -> str:
        payload = {
            'sub': user.email,
            'user_id': user.id,
            'type': AuthTokenEnum.REFRESH_TOKEN.value,
        }
        return jwt_strategy.encode_jwt(
            payload=payload,
            expire_timedelta=timedelta(days=auth_settings.auth_refresh_token_expire_days),
        )

    @staticmethod
    def set_refresh_token_to_cookie(response: Response, refresh_token: str) -> None:
        response.set_cookie(
            key=AuthTokenEnum.REFRESH_TOKEN.value,
            value=refresh_token,
            httponly=True,
            secure=True,
            domain=settings.app_host,
            samesite='none' if IS_DEBUG else 'strict',
            expires=int(timedelta(days=auth_settings.auth_refresh_token_expire_days).total_seconds()),
        )


auth_service = AuthService()
