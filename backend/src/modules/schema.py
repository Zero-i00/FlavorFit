import strawberry
from strawberry.tools import merge_types
from modules.user.resolver import UserQuery, UserMutation

Query = merge_types("Query", (
    UserQuery,
))

Mutation = merge_types("Mutation", (
    UserMutation,
))

graphql_schema = strawberry.Schema(
    query=Query,
    mutation=Mutation
)
