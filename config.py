from pydantic import Field

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    jwt_secret_key: str = Field(env="JWT_SECRET_KEY")
    jwt_algo: str = Field(env="JWT_ALGO")
    class Config:
        env_file = ".env"
        
settings = Settings()