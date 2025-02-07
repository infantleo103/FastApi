from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config.settings import Settings

settings = Settings()

# SQLALCHEMY_DATABASE_URL = "postgresql://"+ settings.DB_USERS + ":" + settings.DB_PASSWORDS + "@" + settings.DB_HOSTS + "/" +settings.DB_NAMES
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.DB_USERS}:{settings.DB_PASSWORDS}@{settings.DB_HOSTS}:5432/{settings.DB_NAMES}"

#sqlite:///./sql_app.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db" 
#SQLALCHEMY_DATABASE_URL = "postgresql://postgres:password@localhost:5433/fastapi"



engine = create_engine(
    SQLALCHEMY_DATABASE_URL, pool_pre_ping=True,pool_size=30, max_overflow=100,pool_timeout=40
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

