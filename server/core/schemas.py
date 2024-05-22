from typing import Any

from pydantic import BaseModel


class HTTPError(BaseModel):
    detail: Any


class HTTPSuccess(BaseModel):
    detail: Any
