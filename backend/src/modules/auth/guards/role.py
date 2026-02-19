from config.graphql import ContextInfo
from modules.user.schema import RoleEnum
from strawberry.permission import BasePermission


def HasRole(required_role: RoleEnum):

    class _HasRole(BasePermission):
        message = f"Requires role: {required_role.name}"

        def has_permission(self, source, info: ContextInfo, **kwargs) -> bool:
            user = info.context.user
            return user.role == required_role if user else False

    return _HasRole
