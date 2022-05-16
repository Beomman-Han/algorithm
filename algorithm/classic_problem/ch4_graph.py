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
    
    ## Add undirected edge
    def add_edge(self, edge: Edge) -> None:
        self._edges[edge.u].append(edge)
        self._edges[edge.v].append(edge.reversed())
    
    ## Add edge with index of vertex
    def add_edge_by_indices(self, u: int, v: int) -> None:
        edge : Edge = Edge(u, v)
        self.add_edge(edge)
    
    def add_edge_by_vertices(self, first: V, second: V) -> None:
        u = self._vertices.index(first)
        v = self._vertices.index(second)
        self.add_edge_by_indices(u, v)
    
    def vertex_at(self, index: int) -> V:
        return self._vertices[index]

    def index_of(self, vertex: V) -> int:
        return self._vertices.index(vertex)

    def neighbors_for_index(self, index: int) -> List[V]:
        #return [ self.vertex_at(edge.v) for edge in self._edges[index] ]
        return list(map(self.vertex_at, [edge.v for edge in self._edges[index]]))
    
    def neighbors_for_vertex(self, vertex: V) -> List[V]:
        return self.neighbors_for_index(self.index_of(vertex))
    
    def edges_for_index(self, index: int) -> List[Edge]:
        return self._edges[index]
    
    def edges_for_vertex(self, vertex: V) -> List[Edge]:
        return self.edges_for_index(self.vertex_at(vertex))
    
    def __str__(self) -> str:
        desc : str = ""
        for i in range(self.vertex_count):
            desc += f"{self.vertex_at(i)} -> {self.neighbors_for_index(i)}\n"
        return desc