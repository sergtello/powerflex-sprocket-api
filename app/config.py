from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    database_uri: str
    database_name: str
    database_alias: str

    path_prefix: Optional[str] = ''

    api_key: str

#    class Config:
#        env_file = ".env"


settings = Settings()
