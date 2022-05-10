from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class Pair(Base):
    pair = "pair"


    reserve0 = Column(Integer, primary_key=True, index=True)
    reserve1 = Column(Integer, primary_key=True, index=True)
    token0 = Column(Integer, primary_key=True, index=True)
    token1 = Column(Integer, primary_key=True, index=True)
    fee = Column(Integer, primary_key=True, index=True)
    address = Column(Integer, primary_key=True, index=True)
