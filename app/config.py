from dataclasses import dataclass

from environs import Env


@dataclass
class DatabaseConfig:
    postgres_user: str
    postgres_password: str
    postgres_db: str
    postgres_host: str


@dataclass
class Config:
    db: DatabaseConfig


def load_config(path: str | None = None) -> Config:
    env: Env = Env()
    env.read_env(path)

    return Config(db=DatabaseConfig(
        postgres_user=env('DB_USER'),
        postgres_password=env('DB_PASS'),
        postgres_db=env('DB_NAME'),
        postgres_host=env('DB_HOST')
    ))
