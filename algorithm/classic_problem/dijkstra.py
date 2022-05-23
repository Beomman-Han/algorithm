from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple, TypeVar
import sys
sys.path.insert(0, '.')
from ch4_graph import WeightedGraph, WeightedEdge
from minimum_spanning_tree import WeightedPath, print_weighted_path, PriorityQueue

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


def path_dict_to_path(
    start : int,
    end : int,
    path_dict : Dict[int, WeightedEdge]
    ) -> WeightedPath:
    
    if len(path_dict) == 0:
        return []
    
    edge_path : WeightedPath = []
    e : WeightedEdge = path_dict[end]
    edge_path.append(e)
    while e.u != start:
        e = path_dict[e.u]
        edge_path.append(e)
    return list(reversed(edge_path))


if __name__ == '__main__':
    
    ## test weighted graph
    city_graph : WeightedGraph[str] = WeightedGraph(['시애틀', '샌프란시스코', '로스앤젤레스',
    '리버사이드', '피닉스', '시카고', '보스턴', '뉴욕', '애틀랜타', '마이애미', 
    '댈러스', '휴스턴', '디트로이트', '필라델피아', '워싱턴'])
    
    city_graph.add_edge_by_vertices('시애틀', '시카고', 1737)
    city_graph.add_edge_by_vertices('시애틀', '샌프란시스코', 678)
    city_graph.add_edge_by_vertices('시카고', '리버사이드', 1704)
    city_graph.add_edge_by_vertices('시카고', '댈러스', 805)
    city_graph.add_edge_by_vertices('시카고', '애틀랜타', 588)
    city_graph.add_edge_by_vertices('시카고', '디트로이트', 238)
    city_graph.add_edge_by_vertices('샌프란시스코', '리버사이드', 386)
    city_graph.add_edge_by_vertices('샌프란시스코', '로스앤젤레스', 348)
    city_graph.add_edge_by_vertices('리버사이드', '로스앤젤레스', 50)
    city_graph.add_edge_by_vertices('리버사이드', '피닉스', 307)
    city_graph.add_edge_by_vertices('댈러스', '피닉스', 887)
    city_graph.add_edge_by_vertices('댈러스', '휴스턴', 225)
    city_graph.add_edge_by_vertices('댈러스', '애틀랜타', 721)
    city_graph.add_edge_by_vertices('애틀랜타', '휴스턴', 702)
    city_graph.add_edge_by_vertices('애틀랜타', '워싱턴', 543)
    city_graph.add_edge_by_vertices('애틀랜타', '마이애미', 604)
    city_graph.add_edge_by_vertices('디트로이트', '워싱턴', 396)
    city_graph.add_edge_by_vertices('디트로이트', '뉴욕', 482)
    city_graph.add_edge_by_vertices('디트로이트', '보스턴', 613)
    city_graph.add_edge_by_vertices('로스앤젤레스', '피닉스', 357)
    city_graph.add_edge_by_vertices('피닉스', '휴스턴', 1015)
    city_graph.add_edge_by_vertices('휴스턴', '마이애미', 968)
    city_graph.add_edge_by_vertices('워싱턴', '필라델피아', 123)
    city_graph.add_edge_by_vertices('워싱턴', '마이애미', 923)
    city_graph.add_edge_by_vertices('뉴욕', '보스턴', 190)
    city_graph.add_edge_by_vertices('뉴욕', '필라델피아', 81)
    print(city_graph)

    distances, path_dict = dijkstra(city_graph, '로스앤젤레스')
    
    name_distance : Dict[str, Optional[int]] = \
        distance_array_to_vertex_dict(city_graph, distances)
    
    print('로스앤젤레스에서의 거리:')
    for key, value in name_distance.items():
        print(f'{key} : {value}')
    print('')
    
    print('로스앤젤레스에서 보스턴까지의 최단 경로:')
    path : WeightedPath = path_dict_to_path(city_graph.index_of('로스앤젤레스'),
                            city_graph.index_of('보스턴'), path_dict)

    print_weighted_path(city_graph, path)