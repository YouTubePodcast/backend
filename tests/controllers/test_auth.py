import pytest
import vcr
from tests.conftest import Secrets

from youtube_podcast_api.controllers.auth import verify_google_auth, hash_string, verify_hash


@pytest.mark.skip
class TestTheAuthModule:
    """Test: The Auth Module..."""

    # NOTE IMPORTANT these will fail:
    # - without correct secretes
    # - simply after a while, because the token will expire
    # - also, when the issued google_id_token will change
    #
    # Test them when needed, but keep them skipped for the most part

    def test_should_return_an_id_with_a_valid_id_token(self, test_secrets: Secrets):
        """It should return an id with a valid id token"""
        with vcr.use_cassette("tests/controllers/cassettes/auth_good"):
            _id = verify_google_auth(test_secrets.google_id_token)
            assert _id == test_secrets.google_user_id

    def test_should_raise_an_error_with_a_bad_id_token(self):
        """It should raise an error with a bad id token"""
        with vcr.use_cassette("tests/controllers/cassettes/auth_bad"):
            with pytest.raises(ValueError):
                verify_google_auth("bad_token")


class TestAuthHashes:
    """Test: Auth Hashes..."""

    def test_should_be_able_to_hash_and_verify_a_string(self):
        """It should be able to hash and verify a string"""
        hashed = hash_string("google_id")
        assert verify_hash("google_id", hashed)
        assert not verify_hash("gogle_id", hashed)
