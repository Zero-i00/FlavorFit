import strawberry


@strawberry.type
class ReactionQuery:

    @strawberry.field
    def placeholder(self) -> str:
        return "reactions"


@strawberry.type
class ReactionMutation:

    @strawberry.field
    def placeholder(self) -> str:
        return "reactions"
