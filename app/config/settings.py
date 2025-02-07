from dotenv import load_dotenv
from pydantic import BaseSettings
import os

# Load .env file
load_dotenv()

class Settings(BaseSettings):
    DB_NAMES: str 
    DB_USERS: str 
    DB_HOSTS: str
    DB_PORTS: str 
    DB_PASSWORDS: str 
    AWS_ACCESSKEY: str
    AWS_SECRETEKEY: str
    AWS_REGIONS:str
    AWS_FILEFORMAT: str
    S3_BUCKET_NAME:str
    
    ALLOWED_ORIGINS: str = "*"
    ALLOW_METHODS:str="*"
    ALLOW_HEADERS:str="*"
    ALLOW_CREDENTIALS: bool =True

    class Config:
        env_file = ".env"  # Ensure Pydantic loads values from .env
        env_file_encoding = "utf-8"

# Create settings instance
settings = Settings()

# Print values to verify
# print(f"DB_NAME: {settings.DB_NAMES}")
# print(f"DB_USER: {settings.DB_USERS}")
# print(f"DB_HOST: {settings.DB_HOSTS}")
# print(f"DB_PORT: {settings.DB_PORTS}")
# print(f"DB_PASSWORD: {settings.DB_PASSWORDS}")
