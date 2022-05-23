from __future__ import annotations
from dataclasses import dataclass
from queue import PriorityQueue
from typing import Dict, List, Optional, Tuple, TypeVar
import sys
sys.path.insert(0, '.')
from ch4_graph import WeightedGraph, WeightedEdge

V = TypeVar('V')


@dataclass
class DijkstraNode:
    vertex : int
    distance : float
    
    def __lt__(self, other : DijkstraNode) -> bool:
        return self.distance < other.distance
    
    def __eq__(self, other : DijkstraNode) -> bool:
        return self.distance == other.distance


def dijkstra(
    wg : WeightedGraph[V],
    root : V
    ) -> Tuple[List[Optional[float]],
               Dict[int, WeightedEdge]]:
    
    first : int = wg.index_of(root)
    distances : List[Optional[float]] = [None] * wg.vertex_count
    distances[first] = 0
    path_dict : Dict[int, WeightedEdge] = {}
    pq : PriorityQueue[DijkstraNode] = PriorityQueue()
    pq.push(DijkstraNode(first, 0))
    
    while not pq.empty:
        u : int = pq.pop().vertex
        dist_u : float = distances[u]
        
        for we in wg.edges_for_index(u):
            dist_v : float = distances[we.v]
            if dist_v is None or dist_v > we.weight + dist_u:
                distances[we.v] = we.weight + dist_u
                path_dict[we.v] = we
                pq.push(DijkstraNode(we.v, we.weight + dist_u))
    
    return distances, path_dict


def distance_array_to_vertex_dict(
    wg : WeightedGraph[V],
    distances : List[Optional[float]]
    ) -> Dict[V, Optional[float]]:
    
    distance_dict : Dict[V, Optional[float]] = {}
    for i in range(len(distances)):
        distance_dict[wg.vertex_at(i)] = distances[i]
    return distance_dict