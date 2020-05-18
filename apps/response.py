import ujson

import settings
from pydantic import typing
from starlette.responses import PlainTextResponse

from paralib.encrypt import AESUtil


class AesResponse(PlainTextResponse):
    def render(self, content: typing.Any) -> bytes:
        if not settings.DEBUG:
            return AESUtil(settings.API_SECRET).encrypt_data(ujson.dumps(content)).encode()
        self.media_type = 'application/json'
        return super(AesResponse, self).render(ujson.dumps(content))
