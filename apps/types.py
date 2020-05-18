from pydantic import BaseModel, PositiveInt, conint


class Pager(BaseModel):
    limit: PositiveInt = 10
    offset: conint(ge=-1) = 0
