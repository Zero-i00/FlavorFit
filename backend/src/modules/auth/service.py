from fastapi import (
    status,
    HTTPException
)


from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models.user import UserModel
from modules.user.service import user_service
from modules.user.schema import UserInput, UserOutput

from modules.auth.strategy.jwt_token import jwt_strategy
from modules.auth.schema import AuthInput, AuthOutput, AuthTokenEnum

class AuthService:

    async def me(self, session: AsyncSession) -> UserOutput:
        ...

    async def register(self, session: AsyncSession, data: AuthInput) -> AuthOutput:
        data.email = data.email.lower()

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
        data.email = data.email.lower()

        query = select(UserModel).where(UserModel.email == data.email)
        result = await session.execute(query)

        existing = result.scalar_one_or_none()

        if existing is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'Пользователя с почтой {data.email} не существует'
            )
        
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


    @staticmethod
    def create_access_token(user: UserOutput) -> str:
        payload = {
            'sub': user.email,
            'role': user.role,
            'user_id': user.id,
            'email': user.email,
            'type': AuthTokenEnum.ACCESS_TOKEN.name
        }

        return jwt_strategy.encode_jwt(payload)


auth_service = AuthService()
