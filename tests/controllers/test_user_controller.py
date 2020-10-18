from unittest.mock import patch
from youtube_podcast_api.controllers.user import AlreadyThereException
import pytest

from tests.typing import YTPTest

from youtube_podcast_api.models.user import User
from youtube_podcast_api.controllers.auth import verify_hash


@pytest.mark.usefixtures("reset_db_after", "UC")
class TestAUserController(YTPTest):
    """Test: A User Controller..."""

    def test_should_be_able_to_create_a_new_user(self, count):
        """It should be able to create a new user"""
        counted = count(User)
        user = self.UC._new_user("google_id")
        assert isinstance(user, User)
        assert verify_hash("google_id", user.hashed_google_id)
        assert count(User) == counted + 1

    def test_should_create_a_user_with_a_valid_id_token(self):
        """It should create a user with a valid id token"""
        def dummy(_):
            return "google_id"
        with patch("youtube_podcast_api.controllers.user.verify_google_auth", new=dummy):
            from youtube_podcast_api.schemas.user import UserLogin
            data = UserLogin.construct(idToken="valid_id_token")
            user = self.UC.create_user(data)
            assert verify_hash("google_id", user.hashed_google_id)

    def test_should_recover_the_user_with_get_user(self, with_user0):
        """It should recover the user with get_user"""
        user = with_user0
        searched = self.UC.get_user("test_user0")
        assert user.id == searched.id

    def test_should_return_none_with_a_wrong_google_id(self):
        """It should return none with a wrong google id"""
        assert self.UC.get_user("not_there_user_id") is None

    def test_should_raise_an_exception_if_the_user_is_already_there(self, with_user0):
        """It should raise an exception if the user is already there"""
        with pytest.raises(AlreadyThereException):
            self.UC._new_user("test_user0")

    def test_should_make_a_new_user_as_admin_if_no_admin_exist(self):
        """It should make a new user as admin if no admin exist"""
        user1 = self.UC._new_user("user_1")
        user2 = self.UC._new_user("user_2")
        assert user1.admin is True
        assert user2.admin is False
