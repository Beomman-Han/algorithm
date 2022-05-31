from statistics import mean, pstdev
from typing import Iterable, List, Sequence, Tuple


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