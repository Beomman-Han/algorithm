from __future__ import annotations
from math import sqrt
from statistics import mean, pstdev
from typing import Iterable, Iterator, List, Sequence, Tuple


def zscores(original : Sequence[float]) -> List[float]:
    """Transform data to z-score"""
    avg : float = mean(original)
    std : float = pstdev(original)
    if std == 0:
        return [0] * len(original)
    return [(x - avg) / std for x in original]


class DataPoint:
    def __init__(self, initial : Iterable[float]) -> None:
        self._originals : Tuple[float, ...] = tuple(initial)
        self.dimensions : Tuple[float, ...] = tuple(initial)  ## ?
    
    @property
    def num_dimenstions(self) -> int:
        return len(self.dimensions)
    
    def distance(self, other : DataPoint) -> float:
        combined : Iterator[Tuple[float, float]] = zip(self.dimensions,
            other.dimensions)
        differences : List[float] = [(x - y) ** 2 for x, y in combined]
        return sqrt(sum(differences))
    
    def __eq__(self, other : object) -> bool:
        if not isinstance(other, DataPoint):
            return NotImplemented
        return self.dimensions == other.dimensions
    
    def __repr__(self) -> str:
        return self._originals.__repr__()