"""This is for artificial neural network practice."""

from typing import List
from math import exp


def dot_product(
    xs : List[float],
    ys : List[float]
    ) -> float:
    return sum([x * y for x, y in zip(xs, ys)])