import bcrypt
from typing import List, Optional
from sqlalchemy import select, delete
from strawberry import UNSET
from database.models.user import UserModel
from utils.normalize import normalize_email
from sqlalchemy.ext.asyncio import AsyncSession
from modules.user.schema import (
    UserInput, UserOutput, UserUpdate,
    ProfileOutput, BodyParameterOutput,
)
from database.models.user.user import ProfileModel, BodyParameterModel


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
        query = select(UserModel).where(UserModel.id == id)
        result = await session.execute(query)
        user = result.scalar_one_or_none()

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
        
        if obj.email:
            user.email = normalize_email(obj.email)

        if obj.password:
            user.password = self.hash_password(obj.password)

        if obj.profile:
            if user.profile is None:
                user.profile = ProfileModel(
                    user=user,
                    full_name=obj.profile.full_name if obj.profile else user.email
                )

            for field, value in vars(obj.profile).items():
                if value is UNSET:
                    continue
                    
                if hasattr(user.profile, field):
                    setattr(user.parameters, field, value)

        
        if obj.parameters:
            if user.parameters is None:
                user.parameters = BodyParameterModel(user=user)

            for field, value in vars(obj.parameters).items():
                if value is UNSET:
                    continue

                if hasattr(user.parameters, field):
                    setattr(user.parameters, field, value)

        session.add(user)

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
        profile = None
        if obj.profile is not None:
            p = obj.profile
            profile = ProfileOutput(
                id=p.id,
                full_name=p.full_name,
                age=p.age,
                bio=p.bio,
                user_id=p.user_id,
                gender=p.gender,
            )

        parameters = None
        if obj.parameters is not None:
            bp = obj.parameters
            parameters = BodyParameterOutput(
                id=bp.id,
                height_cm=bp.height_cm,
                weight_kg=bp.weight_kg,
                goal_weight_kg=bp.goal_weight_kg,
                arm_cm=bp.arm_cm,
                chest_cm=bp.chest_cm,
                waist_cm=bp.waist_cm,
                thigh_cm=bp.thigh_cm,
                activity_level=bp.activity_level,
                nutrition_goal=bp.nutrition_goal,
            )

        return UserOutput(
            id=obj.id,
            email=obj.email,
            role=obj.role.value,
            is_active=obj.is_active,
            profile=profile,
            parameters=parameters,
        )
    


user_service = UserService()


