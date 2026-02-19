import strawberry

from modules.reaction.comments.resolver import CommentQuery, CommentMutation


@strawberry.type
class ReactionQuery:

    @strawberry.field
    def comment(self) -> CommentQuery:
        return CommentQuery()



@strawberry.type
class ReactionMutation:

    @strawberry.field
    def comment(self) -> CommentMutation:
        return CommentMutation()