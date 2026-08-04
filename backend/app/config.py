from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    DATABASE_URL: str = "mysql+pymysql://root@localhost:3306/inventory"

    SECRET_KEY: str = ""
    ALGORITHM:str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

     # Email (SMTP)
    MAIL_SERVER: str = "smtp.gmail.com"
    MAIL_PORT: int = 587
    MAIL_USERNAME: str = ""
    MAIL_PASSWORD: str = ""
    MAIL_TLS: bool = True
    MAIL_SSL: bool = False
    MAIL_FROM: str = ""

    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "allow"


# import this to database.py
settings = Settings()