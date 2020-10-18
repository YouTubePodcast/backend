import json
from unittest.mock import patch
from typing import Dict
from attr import dataclass

import pytest
from sqlalchemy.orm import Session


def test_db_session_maker() -> Session:
    def get_test_settings():
        """Patch the settings object so that the test db is used."""
        from youtube_podcast_api.config import Settings
        settings = Settings()
        settings.db_path = "./sql_test.db"
        return settings

    with patch("youtube_podcast_api.config.get_settings", new=get_test_settings), \
            patch("youtube_podcast_api.database.get_settings", new=get_test_settings), \
            patch("youtube_podcast_api.utils.get_settings", new=get_test_settings):
        from youtube_podcast_api.database import SessionLocal
        return SessionLocal


# This early call is needed to make sure that the db used is the test one, since this module will be called
# before any other imports in test files
get_test_db_session = test_db_session_maker()


@pytest.fixture(scope="function")
def reset_db_after(session):
    """Test teardown that clean the db"""
    yield
    _reset_db(session)


def _reset_db(session: Session):
    """Reset the db"""
    session.execute('''DELETE FROM users''')
    session.commit()
    session.close()


@pytest.fixture(scope="session", autouse=True)
def _init_db():
    """Ensure the test DB is always present and starting from scratch."""
    import alembic.config
    import alembic.command
    alembic_cfg = alembic.config.Config('alembic.ini')
    alembic_cfg.attributes['configure_logger'] = False
    alembic.command.upgrade(alembic_cfg, 'head')
    _reset_db(get_test_db_session())


@pytest.fixture(scope="class")
def session(request):
    """Return a db session and make it available to the whole class"""
    session = get_test_db_session()
    request.cls.session = session
    return session


@pytest.fixture(scope="function")
def client():
    """Make available a client to call the api."""
    from youtube_podcast_api.main import app
    from fastapi.testclient import TestClient
    yield TestClient(app)


def valid_google_id(google_id: str = None):
    """This can be used directly as context manager if a specific google_id is needed"""
    def fake_google(id_token: str) -> str:
        if google_id is None:
            return f"ID_FROM_{id_token}"
        else:
            return google_id
    return patch("youtube_podcast_api.controllers.user.verify_google_auth", new=fake_google)


@pytest.fixture(scope="function")
def with_valid_google_id():
    """Fake the whole token authorization by google lib and server"""
    with valid_google_id():
        yield


def get_user0(session: Session):
    """Create a test user or return it if it already exists"""
    from youtube_podcast_api.controllers.user import UserController as UC
    from youtube_podcast_api.models.user import User
    from youtube_podcast_api.utils import verify_hash
    users = session.query(User).all()
    users = list(filter(lambda user: verify_hash("test_user0", user.hashed_google_id), users))
    if len(users) > 0:
        return users[0]
    else:
        user = UC(session)._new_user("test_user0")
        return user


@pytest.fixture(scope="function")
def with_user0(session):
    """Provide a user to a test function"""
    user = get_user0(session)
    yield user


@pytest.fixture(scope="function")
def UC(session, request):
    """Provide a UserController class ready to go"""
    from youtube_podcast_api.controllers.user import UserController
    uc = UserController(session)
    request.cls.UC = uc
    yield uc


@pytest.fixture(scope="function")
def jresp() -> Dict:
    """Fixture wrapper for json_of_response"""
    def _method(response):
        return json_of_response(response)
    return _method


def json_of_response(response):
    """Decode json from response"""
    return json.loads(response.text)


@pytest.fixture(scope="function")
def count(session):
    """
    Count query on the database. The first argument to this fixture must be the db.Model to query, while all other
    kwargs will be used as filters.
    Example: assert count(User, name="test_user") == 1

    :param model: a model class
    :return: integer
    """
    def _count_in_db(cls, **kwargs):
        if len(kwargs) > 0:
            return session.query(cls).filter_by(**kwargs).count()
        else:
            return session.query(cls).count()
    return _count_in_db


@dataclass
class Secrets:
    """Simple key value container"""
    google_id_token: str
    google_user_id: str


@pytest.fixture(scope="function")
def test_secrets() -> Secrets:
    """Load some secrets from a .env.testing file."""
    from dotenv import load_dotenv
    from os import getenv
    from pathlib import Path
    env_path = Path('.') / '.env.testing'
    load_dotenv(dotenv_path=env_path)
    return Secrets(
        google_id_token=getenv("GOOGLE_ID_TOKEN"),
        google_user_id=getenv("GOOGLE_USER_ID")
    )
