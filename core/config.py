from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv


load_dotenv()


class Config(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_HOST: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_PORT: int
    REDIS_NAME: str
    REDIS_PORT: int
    REDIS_PASSWORD: str
    REDIS_USERNAME: str
    SECRET: str

    model_config = SettingsConfigDict(env_file='../.env')

    @property
    def database_connection(self) -> str:
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    @property
    def redis_connection(self) -> str:
        return f"redis://{self.REDIS_USERNAME}:{self.REDIS_PASSWORD}@{self.REDIS_NAME}:{self.REDIS_PORT}/0"


