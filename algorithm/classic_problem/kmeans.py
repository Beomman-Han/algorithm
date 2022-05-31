from __future__ import annotations
from dataclasses import dataclass
from math import sqrt
from statistics import mean, pstdev
from typing import Generic, Iterable, Iterator, List, Sequence, Tuple, TypeVar


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


Point = TypeVar('Point', bound=DataPoint)

class KMeans(Generic[Point]):
    @dataclass
    class Cluster:
        points : List[Point]
        centroid : DataPoint
    
    def __init__(self,
        k : int,
        points : List[Point]
        ) -> None:
        
        if k < 1:
            raise ValueError("k must be >= 1")
        self._points : List[Point] = points
        self._zscore_normalize()
        self._clusters : List[KMeans.Cluster] = []
        for _ in range(k):
            rand_point : DataPoint = self._random_point()
            cluster : KMeans.Cluster = KMeans.Cluster([], rand_point)
            self._clusters.append(cluster)
    
    @property
    def _centroid(self) -> List[DataPoint]:
        return [x.centroid for x in self._clusters]