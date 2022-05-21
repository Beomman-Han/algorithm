from __future__ import annotations
from dataclasses import dataclass
from typing import TypeVar

V = TypeVar('V')


@dataclass
class DijkstraNode:
    vertex : int
    distance : float
    
    def __lt__(self, other : DijkstraNode) -> bool:
        return self.distance < other.distance
    
    def __eq__(self, other : DijkstraNode) -> bool:
        return self.distance == other.distance