from heapq import heappop, heappush
from typing import Generic, List, TypeVar


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