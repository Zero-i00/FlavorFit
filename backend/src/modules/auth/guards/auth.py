from config.graphql import ContextInfo
from strawberry.permission import BasePermission

class IsAuthenticated(BasePermission):
    message = 'Authentication required'

    def has_permission(self, source, info: ContextInfo, **kwargs) -> bool:
        return info.context.user is not None
