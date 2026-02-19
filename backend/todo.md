# Корректировки в архитектуру backend приложения

Ниже будут описаны новые архитекатурные решения. Твоя задача исправить мои схемы, сервисы и резолверы, следую этим правилам

## Исправления
1. Нужно проверить все написанные файлы schema.py и проверить, что они соответствуют своим моделям и связям. Например, логично верно, что вместе с комментарием, должен отдаваться объект пользователя, который написал этот комментарий
2. Переделываем файлы serivce.py. Основная концепция переделывания заключается в том, что service работает только с моделями, то есть мы нее должны например возвращать UserOutput или CommentOutput при создании или обновлении. Сервис признан работать только с моделями, а значит мы должны вернуть UserModel или CommentModel. Пример реализации такого сервиса, по новой архитектуре
```python
import bcrypt
from fastapi import (
    status,
    HTTPException
)

from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models.user import UserModel
from modules.user.schema import UserSchemaOut, UserSchemaIn, UserSchemaUpdate
from utils.normalize import normalize_email


class UserService:
    def __init__(self) -> None:
        self.not_found_exception = HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

        self.already_exists_exception = HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already exists"
        )


    async def list(self, session: AsyncSession) -> Sequence[UserModel]:
        query = select(UserModel)
        result = await session.execute(query)

        return result.scalars().all()

    async def retrieve(self, session: AsyncSession, user_id: int) -> type[UserModel]:
        user = await session.get(UserModel, user_id)
        if user is None:
            raise self.not_found_exception

        return user

    async def get_by_email(self, session: AsyncSession, email: str) -> type[UserModel]:
        query = select(UserModel).where(UserModel.email == email)
        result = await session.execute(query)

        user = result.scalars().one_or_none()
        if user is None:
            raise self.not_found_exception

        return user


    async def create(self, session: AsyncSession, obj: UserSchemaIn) -> UserModel:
        user = self.to_model(obj)
        user.password = self.hash_password(obj.password)

        session.add(user)
        await session.commit()
        await session.refresh(user)

        return user

    async def update(self, session: AsyncSession, user_id: int, obj: UserSchemaUpdate) -> type[UserModel]:
        user = await self.retrieve(session, user_id)

        if obj.email:
            user.email = normalize_email(str(obj.email))

        if obj.full_name:
            user.full_name = obj.full_name

        session.add(user)
        await session.commit()
        await session.refresh(user)

        return user

    async def destroy(self, session: AsyncSession, user_id: int) -> bool:
        user = await self.retrieve(session, user_id)
        await session.delete(user)
        return True


    @staticmethod
    def hash_password(password: str) -> bytes:
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode(), salt)

    @staticmethod
    def validate_password(password: str, hashed_password: bytes) -> bool:
        return bcrypt.checkpw(password.encode(), hashed_password)

    @staticmethod
    def to_schema(obj: UserModel) -> UserSchemaOut:
        return UserSchemaOut.model_validate(obj)

    @staticmethod
    def to_model(obj: UserSchemaIn) -> UserModel:
        return UserModel(
            email=normalize_email(str(obj.email)),
            full_name=obj.full_name,
        )


user_service = UserService()

```
3. Все exception, которые касаются доменной области, выносим в __init__ сервиса, например not_found_exception, already_exists_exception. А вот пример похожего сервиса, только для авторизации
```python
from datetime import timedelta

import jwt
from fastapi import (
    status,
    Request,
    Response,
    HTTPException, Depends
)
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from config import settings, IS_DEBUG
from database.models.user import UserModel
from modules.auth.schema import AuthSchemaIn, TokenEnum
from modules.auth.strategies.token import token_strategy
from modules.user.service import user_service
from utils.normalize import normalize_email

http_bearer = HTTPBearer()

class AuthService:
    def __init__(self) -> None:
        self.invalid_token_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid jwt token",
        )

        self.invalid_login_or_password_exception = HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid username or password",
        )


    async def register(self, session: AsyncSession, data: AuthSchemaIn) -> UserModel:
        is_exist = await user_service.get_by_email(session, data.email)
        if is_exist:
            raise user_service.already_exists_exception()

        user = await user_service.create(session, data)
        return user

    async def login(self, session: AsyncSession, data: AuthSchemaIn) -> UserModel:
        data.email = normalize_email(str(data.email))

        user = await user_service.get_by_email(session, data.email)

        if not user_service.validate_password(data.password, user.password):
            raise self.invalid_login_or_password_exception

        return user

    async def logout(self, session: AsyncSession) -> None:
        # TODO jwt refresh token black list
        pass


    async def refresh(self, session: AsyncSession, request: Request) -> UserModel:
        payload = self.get_refresh_payload(request)

        user_id = payload.get('user_id', None)
        if user_id is None:
            raise self.invalid_token_exception

        user = await user_service.retrieve(session, user_id)
        return user

    def get_access_token_payload(self, credentials: HTTPAuthorizationCredentials = Depends(http_bearer)) -> dict:
        access_token = credentials.credentials

        try:
            return token_strategy.decode_jwt(
                token=access_token
            )
        except jwt.InvalidTokenError as e:
            raise self.invalid_token_exception

    def get_refresh_payload(self, reqeust: Request) -> dict:
        token = reqeust.cookies.get(TokenEnum.REFRESH_TOKEN.value, None)
        if token is None:
            raise self.invalid_token_exception

        payload = token_strategy.decode_jwt(token)
        if payload is None:
            raise self.invalid_token_exception

        return payload


    @staticmethod
    def create_access_token(user: UserModel) -> str:
        payload = {
            'sub': user.email,
            'role': user.role,
            'user_id': user.id,
            'email': user.email,
            'type': TokenEnum.ACCESS_TOKEN.value
        }

        return token_strategy.encode_jwt(payload)

    @staticmethod
    def create_refresh_token(user: UserModel) -> str:
        payload = {
            'sub': user.email,
            'user_id': user.id,
            'type': TokenEnum.REFRESH_TOKEN.value
        }

        return token_strategy.encode_jwt(
            payload=payload,
            expire_timedelta=timedelta(days=settings.auth.refresh_token_expire_days)
        )

    @staticmethod
    def set_refresh_token_to_cookie(response: Response, refresh_token: str):
        response.set_cookie(
            key=TokenEnum.REFRESH_TOKEN.value,
            value=refresh_token,
            httponly=True,
            secure=True,
            domain=settings.app.host,
            samesite='none' if IS_DEBUG else 'strict',
            expires=int(timedelta(days=settings.auth.refresh_token_expire_days).total_seconds())
        )


auth_service = AuthService()

```
4. Переносим все различные валидации входных данных и приведение Input, Output, Update типов на сторону resolver. ПРиведу пример rest api, но конечно же в нашем случае мы используем GraphQL

```python
from fastapi import (
    status,
    Request,
    Response,
    APIRouter,
)
from database.session import AsyncSessionDep
from modules.auth.schema import AuthSchemaOut, AuthSchemaIn
from modules.auth.service import auth_service


class AuthResolver:


    router = APIRouter(
        prefix="/auth",
        tags=["Auth"],
    )


@staticmethod
@router.post("/register", status_code=status.HTTP_200_OK)
async def register(
        response: Response,
        session: AsyncSessionDep,
        data: AuthSchemaIn
) -> AuthSchemaOut:
    user = await register(session, data)

    access_token = auth_service.create_access_token(session)

    refresh_token = auth_service.create_refresh_token(session)
    auth_service.set_refresh_token_to_cookie(response, refresh_token)

    return AuthSchemaOut(
        user=user,
        access_token=access_token,
    )


@staticmethod
@router.post("/login", status_code=status.HTTP_200_OK)
async def login(
        response: Response,
        session: AsyncSessionDep,
        data: AuthSchemaIn
) -> AuthSchemaOut:
    user = await auth_service.login(session, data)

    access_token = auth_service.create_access_token(session)

    refresh_token = auth_service.create_refresh_token(session)
    auth_service.set_refresh_token_to_cookie(response, refresh_token)

    return AuthSchemaOut(
        user=user,
        access_token=access_token,
    )


@staticmethod
@router.post("/logout", status_code=status.HTTP_200_OK)
async def logout(
        session: AsyncSessionDep,
) -> None:
    await auth_service.logout(session)


@staticmethod
@router.post("/refresh", status_code=status.HTTP_200_OK)
async def refresh(
        request: Request,
        response: Response,
        session: AsyncSessionDep,
) -> AuthSchemaOut:
    user = await auth_service.refresh(session, request)

    access_token = auth_service.create_access_token(session)

    refresh_token = auth_service.create_refresh_token(session)
    auth_service.set_refresh_token_to_cookie(response, refresh_token)

    return AuthSchemaOut(
        user=user,
        access_token=access_token,
    )


auth_resolver = AuthResolver()

```
5. При переписывании логиги возможно придётся добавлять lazy="selectin" параметр в модели - делай при необходимости
6. Нужно вынести comment домен из reaction в домен recipe (положи на одном уровене с ingredients)

Если у тебя есть вопросы - задавай
