from statistics import mean, pstdev
from typing import List, Sequence


def zscores(original : Sequence[float]) -> List[float]:
    """Transform data to z-score"""
    avg : float = mean(original)
    std : float = pstdev(original)
    if std == 0:
        return [0] * len(original)
    return [(x - avg) / std for x in original]