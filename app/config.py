from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    database_uri: Optional[str] = None
    database_name: str

    path_prefix: Optional[str] = ''

    api_key: str

    docs_auth_username: Optional[str] = 'admin'
    docs_auth_password: Optional[str] = 'admin'

    mongodb_root_user: Optional[str] = 'admin'
    mongodb_root_password: Optional[str] = 'admin'

    # class Config:
    #     env_file = ".env"


settings = Settings()
