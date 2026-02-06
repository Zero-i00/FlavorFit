import jwt
import uuid
from datetime import datetime, timedelta
from config.settings import auth_settings

class JWTStrategy:
    
    @staticmethod
    def encode_jwt(
        payload: dict,
        private_key: str = auth_settings.private_key_path.read_text(),
        algorithm: str = auth_settings.auth_algorithm,
        expire_minutes: int = auth_settings.auth_access_token_expire_minutes,
        expire_timedelta: timedelta | None = None
    ):
        now = datetime.utcnow()
        to_encode = payload.copy()

        if expire_timedelta:
            expire = now + expire_timedelta
        else:
            expire = now + timedelta(minutes=expire_minutes)

        to_encode.update(
            iat=int(now.timestamp()),
            exp=int(expire.timestamp()),
            jti=str(uuid.uuid4())
        )

        return jwt.encode(to_encode, private_key, algorithm=algorithm)

    @staticmethod
    def decode_jwt(
        token: str | bytes,
        public_key: str = auth_settings.public_key_path.read_text(),
        algorithm: str = auth_settings.auth_algorithm,
    ):
        return jwt.decode(token, public_key, algorithms=[algorithm])
    

jwt_strategy = JWTStrategy()
