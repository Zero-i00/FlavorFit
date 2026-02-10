import strawberry

from modules.user.resolver import UserQuery, UserMutation
from modules.auth.resolver import AuthQuery, AuthMutation


@strawberry.type
class Query:

    @strawberry.field
    def users(self) -> UserQuery:
        return UserQuery()
    
    @strawberry.field
    def auth(self) -> AuthQuery:
        return AuthQuery()
    

@strawberry.type
class Mutation:

    @strawberry.field
    def users(self) -> UserMutation:
        return UserMutation()
    
    @strawberry.field
    def auth(self) -> AuthMutation:
        return AuthMutation()
    
graphql_schema = strawberry.Schema(
    query=Query,
    mutation=Mutation
)
