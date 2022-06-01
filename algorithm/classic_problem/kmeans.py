from __future__ import annotations
from copy import deepcopy
from dataclasses import dataclass
from functools import partial
from math import sqrt
from random import uniform
from statistics import mean, pstdev
from typing import Generic, Iterable, Iterator, List, Sequence, Tuple, TypeVar


def zscores(original : Sequence[float]) -> List[float]:
    """Transform data to z-score"""
    avg : float = mean(original)
    std : float = pstdev(original)
    if std == 0:
        return [0] * len(original)
    return [(x - avg) / std for x in original]


class DataPoint:
    def __init__(self, initial : Iterable[float]) -> None:
        self._originals : Tuple[float, ...] = tuple(initial)
        self.dimensions : Tuple[float, ...] = tuple(initial)  ## ?
    
    @property
    def num_dimensions(self) -> int:
        return len(self.dimensions)
    
    def distance(self, other : DataPoint) -> float:
        combined : Iterator[Tuple[float, float]] = zip(self.dimensions,
            other.dimensions)
        differences : List[float] = [(x - y) ** 2 for x, y in combined]
        return sqrt(sum(differences))
    
    def __eq__(self, other : object) -> bool:
        if not isinstance(other, DataPoint):
            return NotImplemented
        return self.dimensions == other.dimensions
    
    def __repr__(self) -> str:
        return self._originals.__repr__()


Point = TypeVar('Point', bound=DataPoint)

class KMeans(Generic[Point]):
    @dataclass
    class Cluster:
        points : List[Point]
        centroid : DataPoint
    
    def __init__(self,
        k : int,
        points : List[Point]
        ) -> None:
        
        if k < 1:
            raise ValueError("k must be >= 1")
        self._points : List[Point] = points
        self._zscore_normalize()
        self._clusters : List[KMeans.Cluster] = []
        for _ in range(k):
            rand_point : DataPoint = self._random_point()
            cluster : KMeans.Cluster = KMeans.Cluster([], rand_point)
            self._clusters.append(cluster)
    
    @property
    def _centroids(self) -> List[DataPoint]:
        return [x.centroid for x in self._clusters]
    
    def _dimension_slice(self, dimension : int) -> List[float]:
        ## returns value of column from points
        return [x.dimensions[dimension] for x in self._points]
    
    def _zscore_normalize(self) -> None:
        zscored : List[List[float]] = [[] for _ in range(len(self._points))]
        for dimension in range(self._points[0].num_dimensions):
            dimension_slice : List[float] = self._dimension_slice(dimension)
            for index, zscore in enumerate(zscores(dimension_slice)):
                zscored[index].append(zscore)
                
        for i in range(len(self._points)):
            self._points[i].dimensions = tuple(zscored[i])
    
    def _random_point(self) -> DataPoint:
        ## return random data point within whole dataset
        rand_dimensions : List[float] = []
        for dimension in range(len(self._points[0].dimensions)):
            values : List[float] = self._dimension_slice(dimension)
            rand_value : float = uniform(min(values), max(values))
            rand_dimensions.append(rand_value)
            
        return DataPoint(rand_dimensions)

    def _assign_clusters(self) -> None:
        """find a cluster which of centroid is the closest to
        each data point and allocate the point to the cluster."""
        
        for point in self._points:
            closest_centroid : DataPoint = min(self._centroids,
                                    key=partial(DataPoint.distance, point))
            index : int = self._centroids.index(closest_centroid)
            cluster : KMeans.Cluster = self._clusters[index]
            cluster.points.append(point)
    
    def _generate_centroids(self) -> None:
        """Update centroids of clusters after allocating data 
        point to cluster"""
        
        for cluster in self._clusters:
            if len(cluster.points) == 0:
                continue
            means : List[float] = []
            for dimension in range(cluster.points[0].num_dimensions):
                dimension_slice : List[float] = [x.dimensions[dimension]
                                                    for x in cluster.points]
                means.append(mean(dimension_slice))
            cluster.centroid = DataPoint(means)
    
    def run(self, max_iterations : int = 100) -> List[KMeans.Cluster]:
        """Run K-menas clustering algorithm"""
        
        for iteration in range(max_iterations):
            ## clear cluster
            for cluster in self._clusters:
                cluster.points.clear()
            self._assign_clusters()
            old_centroids : List[KMeans.Cluster] = deepcopy(self._centroids)
            self._generate_centroids()
            if old_centroids == self._centroids:
                print(f'{iteration}회 반복 후 수렴')
                return self._clusters
        return self._clusters


if __name__ == '__main__':
    point1 : DataPoint = DataPoint([2., 1., 1.])
    point2 : DataPoint = DataPoint([2., 2., 5.])
    point3 : DataPoint = DataPoint([3., 1.5, 2.5])
    kmeans_test : KMeans[DataPoint] = KMeans(2, [point1, point2, point3])
    test_clusters : List[KMeans.Cluster] = kmeans_test.run()
    for index, cluster in enumerate(test_clusters):
        print(f'군집 {index}: {cluster.points}')