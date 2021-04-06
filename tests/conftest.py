from fastapi.testclient import TestClient
import pytest
from app.main import app
from app.core import config
from app.db.models import User, Dog
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import yaml
from app.db.db import get_db

from app.core.config import get_settings

settings = config.get_settings()

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.user_db}:{settings.password_db}@{settings.host}:{settings.port_db}/{settings.database_testing}"
# SQLALCHEMY_DATABASE_URL = f"postgresql://daniel:root@localhost:5432/rapidog_testing"

_engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
Session = sessionmaker(bind=_engine)
s = Session()
TestBase = declarative_base()
TestBase.metadata.reflect(bind=_engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=_engine)


#
# def get_settings_override():
#     return config.Settings(database="rapidog_testing")
#

@pytest.fixture(scope="function")
def test_app():
    # set up
    # app.dependency_overrides[config.get_settings] = get_settings_override
    app.dependency_overrides[get_db] = overrid_get_db
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture(autouse=True, scope="function")
def recreateDB():
    TestBase.metadata.reflect(bind=_engine)
    TestBase.metadata.drop_all(_engine, checkfirst=True)
    TestBase.metadata.create_all(_engine, checkfirst=True)
    for data in yaml.load_all(open('tests/dummy/users.yaml'), Loader=yaml.FullLoader):
        user = User(**data)
        s.add(user)
    s.commit()

    # for data in yaml.load_all(open('tests/dummy/dogs.yaml'), Loader=yaml.FullLoader):
    #     dog = Dog(**data)
    #     s.add(dog)
    #     s.commit()


def overrid_get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
