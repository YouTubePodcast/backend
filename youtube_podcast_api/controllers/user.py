from typing import Union
from uuid import uuid4
from sqlalchemy.orm import Session

from youtube_podcast_api.controllers.auth import verify_google_auth, hash_string, verify_hash
from youtube_podcast_api.models.user import User
from youtube_podcast_api.schemas.user import UserLogin


class UserController:

    def __init__(self, db: Session):
        self.db: Session = db

    def get_user(self, google_id: str) -> Union[User, None]:
        """Return the user from the given google id"""
        users = self.db.query(User).all()
        selected_users = list(filter(lambda user: verify_hash(google_id, user.hashed_google_id), users))
        if len(selected_users) == 1:
            return selected_users[0]
        else:
            return None

    def create_user(self, user: UserLogin) -> User:
        """Create a user starting from a valid google user id"""
        google_id = verify_google_auth(user.idToken)
        return self._new_user(google_id)

    def _new_user(self, google_id: str) -> User:
        """Create a new User object and add it to the db"""
        if self._does_user_exist(google_id):
            raise AlreadyThereException()
        hashed_google_id = hash_string(google_id)
        token = self.generate_token()
        db_user = User(hashed_google_id=hashed_google_id, token=token)
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    @ staticmethod
    def generate_token():
        """Generate a new uuid4 token"""
        return uuid4().hex

    def _does_user_exist(self, google_id: str) -> bool:
        """Return True if the user with the specified google id exists"""
        return self.get_user(google_id) is not None


class AlreadyThereException(Exception):
    """Raised if a user is already registered."""
