from typing import *
from . import models

class UnshiftableIterable(object):
    def __init__(self, iterable):
        self._iter = iter(iterable)
        self._unshifted = []
    def __iter__(self):
        while True:
            if self._unshifted:
                yield self._unshifted.pop()
            else:
                yield self._iter.next()
    def unshift(self, item):
        self._unshifted.append(item)

class Pair(object):
    QUOTE_MAX_DIFFERENCE = 1e-3

    def __init__(
        self,
        address: str,
        reserve0: int,
        reserve1: int,
        token0: Optional[str] = None,
        token1: Optional[str] = None,
    ):
        self.addresses = [address]
        self.weights: List[int] = []
        self.reserve0 = reserve0
        self.reserve1 = reserve1
        self.token0 = token0
        self.token1 = token1

    def add_pair(self, other: "Pair", weight: int) -> "Pair":
        assert (
            self.token0 is not None and self.token1 is not None
        ), "tokens aren't initialized"
        assert (
            self.token0 == other.token0 and self.token1 == other.token1
        ), "incompatible tokens"
        assert (
            self.quote(self.token0) - other.quote(other.token0)
            <= self.QUOTE_MAX_DIFFERENCE
        ), "quotes differ too much"
        return Pair(
            self.address + other.address,
            self.reserve0 + other.reserve0,
            self.reserve1 + other.reserve1,
            self.token0,
            self.token1,
        )

    def get_threshold(self, in_amount: int, in_token: str, other: "Pair") -> int:
        assert self.get_out_amount(in_amount, in_token) >= other.get_out_amount(
            in_amount, in_token
        ), "wrong order"
        raise NotImplementedError()

    def sort_reserves(self, in_token: str) -> Tuple[bool, int, int]:
        raise NotImplementedError()

    def quote(self, in_token: str) -> int:
        _, in_reserve, out_reserve = self.sort_reserves(in_token)
        return out_reserve / in_reserve

    def get_out_amount(self, in_amount: int, in_token: str) -> int:
        raise NotImplementedError()

    def swap(self, in_amount: int, in_token: str) -> models.Pair:
        _reversed, reserve_in, reserve_out = self.sort_reserves(in_token)
        reserve_in += in_amount
        reserve_out -= self.get_out_amount(in_amount, in_token)
        reserve0, reserve1 = reserve_in, reserve_out
        if _reversed:
            reserve0, reserve1 = reserve1, reserve0
        return Pair(self.address, reserve0, reserve1, self.token0, self.token1)


def get_route_segment(in_amount: int, in_token: str, pairs: List[Pair]):
    key = lambda pair: Pair.get_out_amount(pair, in_amount, in_token)
    pairs = sorted(pairs, key=key)
    pair, *pairs = pairs
    weight = 0
    for _pair in pairs:
        threshold = pair.get_threshold(in_amount, in_token, _pair)
        weight += threshold * 100 / Pair.amount
        if Pair.amount > threshold:
            pair = pair.add_pair(models.Pair.other) 
    raise NotImplementedError()


def get_route(
    in_amount: int,
    in_token: str,
    out_token: str,
    route_map: Dict[str, Dict[str, List[Pair]]],
):
    m: Dict[str, Tuple[int, List[Pair]]] = {}
    p = [in_token]
    while len(p):
        token = p.pop()
        for next_token, pairs in route_map.get(token, []):
            next_amount = int("compute split trade")
            amount, seg = m.get(next_token, (0, []))
            if next_amount > amount:
                m[next_token] = [next_amount, pairs]
                p.insert(0, next_token)
                if(next_token != out_token):
                    _p = UnshiftableIterable(p)
    Tuple[int, List[Pair]] = m.get(out_token)
    outAmount = seg.outAmount
    segments = []
    while Tuple[List[Pair]] == in_token:
        segments.append(seg)
        Tuple[int, List[Pair]] = m.get(Tuple[List[Pair]])
    return segments and outAmount