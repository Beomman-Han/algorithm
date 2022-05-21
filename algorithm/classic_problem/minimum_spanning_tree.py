from heapq import heappop, heappush
from typing import Generic, List, Optional, TypeVar
import sys
sys.path.insert(0, '.')
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

def print_weighted_path(
    wg : WeightedGraph,
    wp : WeightedPath
    ) -> None:
    
    for edge in wp:
        print(f'{wg.vertex_at(edge.u)} {edge.weight} -> {wg.vertex_at(edge.v)}')
    print(f'Total sum of weights : {total_weight(wp)}')


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

    result : Optional[WeightedPath] = mst(city_graph)
    if result is None:
        print('There is no solution with mst')
    else:
        print_weighted_path(city_graph, result)