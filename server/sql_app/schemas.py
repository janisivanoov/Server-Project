from typing import List, Optional
from uint import Uint, Int
from pydantic import BaseModel

class PairBase(BaseModel):
    reserve0: Uint
    reserve1: Uint
    token0: hex(20)
    token1: hex(20)
    fee: Uint
    address: hex(20)


class PairCreate(PairBase):
    pass


class Pair(PairBase):
    reserve0: Uint
    reserve1: Uint
    token0: hex(20)
    token1: hex(20)
    fee: Uint
    address: hex(20)
    pair_id: int

    class Config:
        orm_mode = True