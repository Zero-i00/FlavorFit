import strawberry
from strawberry.tools import merge_types

from modules.user.resolver import UserQuery, UserMutation
from modules.auth.resolver import AuthQuery, AuthMutation

Query = merge_types("Query", (
    UserQuery,
    AuthQuery,
))

Mutation = merge_types("Mutation", (
    UserMutation,
    AuthMutation,
))

graphql_schema = strawberry.Schema(
    query=Query,
    mutation=Mutation
)
