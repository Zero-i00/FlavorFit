from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).parent.parent

class PostgresSettings(BaseSettings):
    postgres_host: str = 'localhost'
    postgres_port: int = 5432
    postgres_db: str = 'flavor_fit_db'
    postgres_user: str = 'postgres'
    postgres_password: str = '12345678'

    @property
    def DATABASE_URL(self):
        return f'postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}'

    model_config = SettingsConfigDict(
        env_file=BASE_DIR.parent / ".env",
        case_sensitive=False,
        extra="ignore"
    )


class AuthSettings(BaseSettings):
    auth_secret_key: str = 'secret'
    auth_algorithm: str = "RS256"
    auth_access_token_expire_minutes: int = 15
    auth_refresh_token_expire_days: int = 30

    private_key_path: Path = BASE_DIR / 'certs' / 'jwt-private.pem'
    public_key_path: Path = BASE_DIR / 'certs' / 'jwt-public.pem'

    model_config = SettingsConfigDict(
        env_file=BASE_DIR.parent / ".env",
        case_sensitive=False,
        extra="ignore"
    )


class Settings(BaseSettings):
    app_port: int = 8000
    app_host: str = 'localhost'
    app_name: str = 'Flavor Fit'
    app_mode: str = 'DEVELOPING'

    model_config = SettingsConfigDict(
        env_file=BASE_DIR.parent / ".env",
        case_sensitive=False,
        extra="ignore"
    )


settings = Settings()
auth_settings = AuthSettings()
database_settings = PostgresSettings()

IS_DEBUG = settings.app_mode == 'DEVELOPING'
