from heapq import heappop, heappush
from typing import Generic, List, Optional, TypeVar
import sys
sys.path.insert('.', 0)
from ch4_graph import WeightedEdge, WeightedGraph


T = TypeVar('T')

class PriorityQueue(Generic[T]):
    def __init__(self) -> None:
        self._container : List[T] = []
    
    @property
    def empty(self) -> bool:
        return not self._container
    
    def push(self, item : T) -> None:
        heappush(self._container, item)
    
    def pop(self) -> T:
        return heappop(self._container)
    
    def __repr__(self) -> str:
        return repr(self._container)


V = TypeVar('V')
WeightedPath = List[WeightedEdge]  ## type alias for minimum spanning tree

def total_weight(wp : WeightedPath) -> float:
    return sum([edge.weight for edge in wp])

def mst(
    wg : WeightedGraph,
    start : int = 0
    ) -> Optional[WeightedPath]:
    
    if start > wg.vertex_count - 1 or start < 0:
        return None
    
    result : WeightedPath = []  ## mst result
    pq : PriorityQueue[WeightedEdge] = PriorityQueue()
    visited : List[bool] = [False] * wg.vertex_count
    
    def visit(index : int):
        visited[index] = True
        for edge in wg.edges_for_index(index):
            if not visited[edge.v]:
                pq.push(edge)
    
    visit(start)
    
    while not pq.empty:
        edge = pq.pop()
        if visited[edge.v]:
            continue
        result.append(edge)
        visit(edge.v)
    
    return result