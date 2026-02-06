import strawberry
from enum import Enum
from modules.user.schema import UserOutput

@strawberry.enum
class AuthTokenEnum(Enum):
    ACCESS_TOKEN = 'access_token'
    REFRESH_TOKEN = 'refresh_token'


@strawberry.enum
class TokenType(Enum):
    BEARER = "Bearer"

@strawberry.input
class AuthInput:
    email: str
    password: str


@strawberry.type
class AuthOutput:
    user: UserOutput
    access_token: str
    token_type: TokenType = TokenType.BEARER
