from datetime import timedelta
from typing import Any, Optional
from fastapi import (
    Request,
    status,
    Response,
    HTTPException
)

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models.user import UserModel
from modules.user.service import user_service
from modules.user.schema import UserInput, UserOutput

from modules.auth.strategies.jwt_token import jwt_strategy
from modules.auth.schema import AuthInput, AuthOutput, AuthTokenEnum

from config.settings import settings, auth_settings, IS_DEBUG

from utils.normalize import normalize_email


class AuthService:
    def __init__(self) -> None:
        self.invalid_token_exception = HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid jwt token",
            )
        
        self.user_not_found_exception = HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found'
        )
    

    async def register(self, session: AsyncSession, data: AuthInput) -> AuthOutput:
        data.email = normalize_email(data.email)

        is_exist = await user_service.get_by_email(session, data.email)
        if is_exist:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Пользователь с такой почтой уже существует'
            )
        
        user = await user_service.create(session, UserInput(
            email=data.email,
            password=data.password
        ))

        access_token = self.create_access_token(user)

        return AuthOutput(
            user=user,
            access_token=access_token
        )


    async def login(self, session: AsyncSession, data: AuthInput) -> AuthOutput:
        data.email = normalize_email(data.email)

        query = select(UserModel).where(UserModel.email == data.email)
        result = await session.execute(query)

        existing = result.scalar_one_or_none()

        if existing is None:
            raise self.user_not_found_exception
        
        if not user_service.validate_password(data.password, existing.password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Неверный логин или пароль'
            )
        
        user = user_service.to_schema(existing)

        access_token = self.create_access_token(user)

        return AuthOutput(
            user=user,
            access_token=access_token
        )

    async def refresh_token(self, session: AsyncSession, request: Request) -> AuthOutput:
        payload = self.get_token_payload(
            request=request, 
            token_type=AuthTokenEnum.REFRESH_TOKEN
        )

        user_id = payload.get('user_id', None)
        if user_id is None:
            raise self.user_not_found_exception

        user = await user_service.retrieve(session, int(user_id))
        if user is None:
            raise self.user_not_found_exception

        access_token = self.create_access_token(user)

        return AuthOutput(
            user=user,
            access_token=access_token
        )
    
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
                print(token)
                if token is None:
                    raise self.invalid_token_exception
            case _:
                raise self.invalid_token_exception
        
        payload = jwt_strategy.decode_jwt(token)
        if payload is None:
            raise self.invalid_token_exception
        
        return payload


    @staticmethod
    def create_access_token(user: UserOutput) -> str:
        payload = {
            'sub': user.email,
            'role': user.role,
            'user_id': user.id,
            'email': user.email,
            'type': AuthTokenEnum.ACCESS_TOKEN.value
        }

        return jwt_strategy.encode_jwt(payload)
    

    @staticmethod
    def create_refresh_token(user: UserOutput) -> str:
        payload = {
            'sub': user.email,
            'user_id': user.id,
            'type': AuthTokenEnum.REFRESH_TOKEN.value
        }

        return jwt_strategy.encode_jwt(
            payload=payload,
            expire_timedelta=timedelta(days=auth_settings.auth_refresh_token_expire_days)
        )
    
    @staticmethod
    def set_refresh_token_to_cookie(response: Response, refresh_token: str):
        response.set_cookie(
            key=AuthTokenEnum.REFRESH_TOKEN.value,
            value=refresh_token,
            httponly=True,
            secure=True,
            domain=settings.app_host,
            samesite='none' if IS_DEBUG else 'strict',
            expires=int(timedelta(days=auth_settings.auth_refresh_token_expire_days).total_seconds())
        )


auth_service = AuthService()
