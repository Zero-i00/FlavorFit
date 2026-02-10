import bcrypt
from typing import List, Optional
from sqlalchemy import select, delete
from database.models.user import UserModel
from sqlalchemy.ext.asyncio import AsyncSession
from modules.user.schema import UserInput, UserOutput, UserUpdate


class UserService:

    async def list(self, session: AsyncSession) -> List[UserOutput]:
        query = select(UserModel)
        result = await session.execute(query)

        users = result.scalars().all()

        return [
            self.to_schema(user)
            for user in users
        ]
    
    async def retrieve(self, session: AsyncSession, id: int) -> Optional[UserOutput]:
        user = await session.get(UserModel, id)

        return self.to_schema(user) if user else None
    

    async def get_by_email(self, session: AsyncSession, email: str) -> Optional[UserOutput]:
        query = select(UserModel).where(UserModel.email == email)
        result = await session.execute(query)

        user = result.scalar_one_or_none()
        return self.to_schema(user) if user else None
    
    async def create(self, session: AsyncSession, obj: UserInput) -> UserOutput:
        user = UserModel(
            email=obj.email,
            password=self.hash_password(obj.password)
        )

        session.add(user)
        await session.commit()
        await session.refresh(user)

        return self.to_schema(user)
    
    async def update(self, session: AsyncSession, id: int, obj: UserUpdate) -> Optional[UserOutput]:
        user = await session.get(UserModel, id)
        if not user:
            return None
    
        for field in UserInput.__annotations__.keys():
            value = getattr(obj, field, None)
            if value is not None and hasattr(user, field):
                setattr(user, field, value)

        await session.commit()
        await session.refresh(user)

        return self.to_schema(user)


    async def destroy(self, session: AsyncSession, id: int) -> None:
        query = delete(UserModel).where(UserModel.id == id)
        await session.execute(query)
        await session.commit()

    @staticmethod
    def hash_password(password: str) -> bytes:
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode(), salt)
    
    @staticmethod
    def validate_password(password: str, hashed_password: bytes) -> bool:
        return bcrypt.checkpw(password.encode(), hashed_password) 

    @staticmethod
    def to_schema(obj: UserModel) -> UserOutput:
        return UserOutput(
            id=obj.id,
            email=obj.email,
            role=obj.role.value,
            is_active=obj.is_active,
        )
    


user_service = UserService()


