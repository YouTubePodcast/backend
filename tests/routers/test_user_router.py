from unittest.mock import patch
from youtube_podcast_api.controllers.user import AlreadyThereException
from tests.typing import CLIENT, JRESP, YTPTest


class TestAUserRouter(YTPTest):
    """Test: A User Router..."""

    def test_should_be_able_to_create_a_new_user(self, client: CLIENT, jresp: JRESP, UC, with_fake_google):
        """It should be able to create a new user"""
        data = {"idToken": "a_id_token"}
        r = client.put("/user/", json=data)
        assert 200 == r.status_code
        assert "token" in jresp(r)
        user = self.UC.get_user(f"ID_FROM_{data.get('idToken')}")
        assert user is not None

    def test_should_409_with_an_already_existing_user(self, client: CLIENT):
        """It should 409 with an already existing user"""
        def dummy(cls, user):
            raise AlreadyThereException()
        with patch("youtube_podcast_api.controllers.user.UserController.create_user", new=dummy):
            r = client.put("/user/", json={"idToken": "test_user0"})
        assert 409 == r.status_code
