from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from . import models


class TestDatabase:
    def setup_class(self):
        self.SQLALCHEMY_DATABASE_URL = "sqlite://"
        self.engine = create_engine(
            self.SQLALCHEMY_DATABASE_URL,
            connect_args={"check_same_thread": False},
            echo=True,
        )
        self.SessionLocal = sessionmaker(
            autoflush=False, autocommit=False, bind=self.engine
        )
        self.Base = declarative_base()
        self.db = self.SessionLocal()
        models.Base.metadata.create_all(bind=self.engine)

    def teardown_class(self):
        self.Base.metadata.drop_all(bind=self.engine)
        self.db.close()

    def test_create_user(self):
        from ..api import schemas
        from .crud import create_user

        timmy_schema = schemas.UserCreate(
            username="timmyt",
            firstname="Timmy",
            lastname="Test",
            email="timmyt@gmail.com",
            is_pi=False,
            sponsor_id=None,
        )
        timmy_user = create_user(self.db, timmy_schema)
        assert (
            timmy_user.username == "timmyt"
            and timmy_user.firstname == "Timmy"
            and timmy_user.lastname == "Test"
            and timmy_user.email == "timmyt@gmail.com"
            and timmy_user.is_pi == False
            and timmy_user.sponsor_id == None
        )
