# This module is used to trick ides and have the right intellisense when testing
from __future__ import annotations

from requests.models import Response
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from youtube_podcast_api.controllers.user import UserController

    class YTPTest:
        """"""
        UC: UserController


class CLIENT:
    def get(self) -> Response: ...
    def put(self) -> Response: ...
    def delete(self) -> Response: ...
    def post(self) -> Response: ...
