from dataclasses import dataclass
from environs import Env


@dataclass
class DatabaseConfig:
    database: str
    db_host: str
    db_user: str
    db_password: str


@dataclass
class TgBot:
    token: str


@dataclass
class Config:
    tg_bot: TgBot


def load_config(path: str | None = None):

    env: Env = Env()
    env.read_env()

    return Config(
        tg_bot=TgBot(
            token=env("BOT_TOKEN"),
        )
    )
