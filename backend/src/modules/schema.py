import strawberry

from modules.user.resolver import UserQuery, UserMutation
from modules.auth.resolver import AuthQuery, AuthMutation

from modules.recipe.resolver import RecipeQuery, RecipeMutation
from modules.reaction.resolver import ReactionQuery, ReactionMutation


@strawberry.type
class Query:

    @strawberry.field
    def users(self) -> UserQuery:
        return UserQuery()

    @strawberry.field
    def recipes(self) -> RecipeQuery:
        return RecipeQuery()

    @strawberry.field
    def reactions(self) -> ReactionQuery:
        return ReactionQuery()

    @strawberry.field
    def auth(self) -> AuthQuery:
        return AuthQuery()


@strawberry.type
class Mutation:

    @strawberry.field
    def users(self) -> UserMutation:
        return UserMutation()

    @strawberry.field
    def recipes(self) -> RecipeMutation:
        return RecipeMutation()

    @strawberry.field
    def reactions(self) -> ReactionMutation:
        return ReactionMutation()

    @strawberry.field
    def auth(self) -> AuthMutation:
        return AuthMutation()

graphql_schema = strawberry.Schema(
    query=Query,
    mutation=Mutation
)
