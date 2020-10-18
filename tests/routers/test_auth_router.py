from tests.conftest import valid_google_id
from tests.typing import YTPTest, CLIENT, JRESP

from youtube_podcast_api.models.user import User


class TestTheAuthRouter(YTPTest):
    """Test: The Auth Router..."""

    def test_should_return_the_token_with_a_valid_id_token(self, with_user0: User, client: CLIENT, jresp: JRESP):
        """It should return the token with a valid id_token"""
        user = with_user0
        with valid_google_id("test_user0"):
            headers = {
                "Bearer": "test_user0_id_token"
            }
            r = client.get("/auth/", headers=headers)
            resp = jresp(r)
            assert r.status_code == 200
            assert user.token == resp["token"]

    def test_should_return_404_if_no_user_are_found(self, client: CLIENT):
        """It should return 404 if no user are found"""
        headers = {
            "Bearer": "test_user0_id_token"
        }
        r = client.get("/auth/", headers=headers)
        assert r.status_code == 404
