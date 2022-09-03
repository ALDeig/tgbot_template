from pydantic import BaseSettings


class DefaultConfig(BaseSettings):
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


class TgBot(DefaultConfig):
    token: str
    admins: list[int]
    use_redis: bool


class DbConfig(DefaultConfig):
    password: str
    user: str
    name: str
    host: str = "127.0.0.1"

    class Config:
        env_prefix = "DB_"


class Settings(BaseSettings):
    tg: TgBot = TgBot()
    db_url: str
    # db: DbConfig = DbConfig()


def get_settings() -> Settings:
    db_config = DbConfig()
    db_url = f"postgresql+asyncpg://{db_config.user}:{db_config.password}@{db_config.host}/{db_config.name}"
    # db_url = f"sqlite+aiosqlite:///{Path('db/db_name.db')
    config = Settings(db_url=db_url)
    return config


