from typing import List, Optional
from pydantic import BaseModel
from sqlalchemy import Integer, CHAR

class PairBase(BaseModel):
    reserve0: Integer
    reserve1: Integer
    token0: CHAR
    token1: CHAR
    fee: Integer
    address: CHAR


class PairCreate(PairBase):
    pass


class Pair(PairBase):
    reserve0: Integer
    reserve1: Integer
    token0: CHAR
    token1: CHAR
    fee: Integer
    address: CHAR
    pair_id: Integer

    class Config:
        orm_mode = True