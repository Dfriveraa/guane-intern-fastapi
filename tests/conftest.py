import pytest
import yaml
from app.db import Base
from app.db import User, Dog
from app.db import get_db
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core import config
from app.main import app

settings = config.get_settings()

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.user_db}:{settings.password_db}@{settings.host}:{settings.port_db}/{settings.database_testing}"
_engine = create_engine(SQLALCHEMY_DATABASE_URL)
Base.metadata.create_all(bind=_engine)
Session = sessionmaker(bind=_engine)
s = Session()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=_engine)


@pytest.fixture(scope="function")
def test_app():
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture(autouse=True, scope="function")
def recreateDB():
    Base.metadata.reflect(bind=_engine)
    Base.metadata.drop_all(_engine, checkfirst=True)
    Base.metadata.create_all(_engine, checkfirst=True)
    for data in yaml.load_all(open('tests/dummy/users.yaml'), Loader=yaml.FullLoader):
        user = User(**data)
        s.add(user)
    s.commit()
    for data in yaml.load_all(open('tests/dummy/dogs.yaml'), Loader=yaml.FullLoader):
        dog = Dog(**data)
        s.add(dog)
    s.commit()


def override_get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
