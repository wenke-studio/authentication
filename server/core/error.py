from pydantic import BaseModel


class HTTPError(BaseModel):
    msg: str
