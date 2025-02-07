from data import models
from data.database import engine, SessionLocal


models.Base.metadata.create_all(bind=engine)


#create SqlAlchemy sessionlocal dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()