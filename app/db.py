from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker

from app.settings import settings

engine = create_engine(url=settings.database_url)
CustomSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class SessionManager:
    session: Session = None

    def __enter__(self):
        self.session = CustomSession()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()
