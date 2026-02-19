import bcrypt
from typing import Optional, Sequence

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from strawberry import UNSET

from database.models import UserModel
from database.models.user import UserModel
from database.models.user.user import ProfileModel, BodyParameterModel
from modules.user.schema import UserInput, UserOutput, UserUpdate
from modules.user.profile.schema import ProfileOutput
from modules.user.parameters.schema import BodyParameterOutput
from utils.normalize import normalize_email


class UserService:
    def __init__(self) -> None:
        self.not_found_exception = HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

        self.already_exists_exception = HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already exists",
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

    async def get_by_email(self, session: AsyncSession, email: str) -> Optional[UserModel]:
        query = select(UserModel).where(UserModel.email == email)
        result = await session.execute(query)
        return result.scalar_one_or_none()

    async def create(self, session: AsyncSession, obj: UserInput) -> UserModel:
        user = UserModel(
            email=normalize_email(obj.email),
            password=self.hash_password(obj.password),
        )

        session.add(user)
        await session.commit()
        await session.refresh(user)

        return user

    async def update(self, session: AsyncSession, user_id: int, obj: UserUpdate) -> UserModel:
        user = await self.retrieve(session, user_id)

        if obj.email is not UNSET and obj.email:
            user.email = normalize_email(obj.email)

        if obj.password is not UNSET and obj.password:
            user.password = self.hash_password(obj.password)

        if obj.profile is not UNSET and obj.profile:
            if user.profile is None:
                user.profile = ProfileModel(
                    user=user,
                    full_name=obj.profile.full_name if obj.profile.full_name is not UNSET else user.email,
                )

            for field, value in vars(obj.profile).items():
                if value is UNSET:
                    continue
                if hasattr(user.profile, field):
                    setattr(user.profile, field, value)

        if obj.parameters is not UNSET and obj.parameters:
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

        return user

    async def destroy(self, session: AsyncSession, id: int) -> bool:
        user = await self.retrieve(session, id)
        await session.delete(user)
        await session.commit()
        return True

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
                user_id=p.user_id,
                age=p.age,
                bio=p.bio,
                gender=p.gender,
            )

        parameters = None
        if obj.parameters is not None:
            bp = obj.parameters
            parameters = BodyParameterOutput(
                id=bp.id,
                user_id=bp.user_id,
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
            role=obj.role,
            is_active=obj.is_active,
            profile=profile,
            parameters=parameters,
        )

    @staticmethod
    def to_model(obj: UserInput) -> UserModel:
        return UserModel(
            email=normalize_email(obj.email),
            password=b'',
        )


user_service = UserService()
