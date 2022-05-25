from abc import ABC, abstractmethod
from typing import Tuple, Type, TypeVar


T = TypeVar('T', bound='Chromosome')

class Chromosome(ABC):
    @abstractmethod
    def fitness(self) -> float: ...
    
    @classmethod
    @abstractmethod
    def random_instance(cls: Type[T]) -> T: ...
    
    @abstractmethod
    def crossover(self: T, other: T) -> Tuple[T, T]: ...
    
    @abstractmethod
    def mutate(self) -> None: ...