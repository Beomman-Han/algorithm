from __future__ import annotations
from dataclasses import dataclass
from typing import Generic, List, TypeVar


@dataclass
class Edge:
    u: int  ## from vertex u, index of vertex
    v: int  ## to vertex v, index of vertex

    def reversed(self) -> Edge:
        return Edge(self.v, self.u)
    
    def __str__(self) -> str:
        return f'{self.u} -> {self.v}'

V = TypeVar('V')

class Graph(Generic[V]):
    def __init__(self, vertices : List[V] = []) -> None:
        self._vertices = vertices
        self._edges = List[List[Edge]] = [[] for _ in vertices]
    
    @property
    def vertex_count(self) -> int:
        return len(self._vertices)
    
    @property
    def edge_count(self) -> int:
        return sum(map(len, self._edges))
    
    ## Add vertex to graph and return index
    def add_vertex(self, vertex: V) -> int:
        self._vertices.append(vertex)
        self._edges.append([])  ## Add empty edge
        return self.vertex_count - 1