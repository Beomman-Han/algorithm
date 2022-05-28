from __future__ import annotations
from abc import ABC, abstractmethod
from copy import deepcopy
from enum import Enum
from heapq import nlargest
from random import choices, random, randrange
from statistics import mean
from typing import Callable, Generic, List, Tuple, Type, TypeVar


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


C = TypeVar('C', bound=Chromosome)

class GeneticAlgorithm(Generic[C]):
    SelectionType = Enum("SelectionType", "ROULETTE TOURNAMENT")
    ## SelectionType = Enum("SelectionType", ("ROULETTE", "TOURNAMENT"))
    
    def __init__(self, 
        initial_population: List[C],
        threshold: float,
        max_generations: int = 100,
        mutation_chance: float = 0.01,
        crossover_chance: float = 0.7,
        selection_type: SelectionType = SelectionType.TOURNAMENT
        ) -> None:
        
        self._population = initial_population
        self._threshold = threshold
        self._max_generations = max_generations
        self._mutation_chance = mutation_chance
        self._crossover_chance = crossover_chance
        self._selection_type = selection_type
        self._fitness_key : Callable = type(self._population[0]).fitness
    
    def _pick_roulette(self, wheel: List[float]) -> Tuple[C, C]:
        return tuple(choices(self._population, weights=wheel, k=2))
    
    def _pick_tournament(self, num_participants : int) -> Tuple[C, C]:
        ## pick chromosomes of num_participants randomly
        participants : List[C] = choices(self._population, k=num_participants)
        return tuple(nlargest(2, participants, key=self._fitness_key))
    
    def _reproduce_and_replace(self) -> None:
        ## replace existing population to new population
        new_population : List[C] = []
        
        while len(new_population) < len(self._population):
            if self._selection_type == GeneticAlgorithm.SelectionType.ROULETTE:
                parents : Tuple[C, C] = self._pick_roulette(
                    [x.fitness() for x in self._population])
            else:
                parents : Tuple[C, C] = self._pick_tournament(
                    len(self._population) // 2)
            ## crossover
            if random() < self._crossover_chance:
                new_population.extend(parents[0].crossover(parents[1]))
            else:
                new_population.extend(parents)
        ## If num of population is odd, num of new population must be 
        ## larger than previous population.
        if len(new_population) > len(self._population):
            new_population.pop()
        self._population = new_population
    
    def _mutate(self) -> None:
        ## mutate each chromosome by mutation chance
        for individual in self._population:
            if random() < self._mutation_chance:
                individual.mutate()
    
    def run(self) -> C:
        ## run genetic algorithm by max generation,
        ## return chromosome with the best fitness.
        best : C = max(self._population, key=self._fitness_key)
        for generation in range(self._max_generations):
            if best.fitness() >= self._threshold:
                return best
            print(f'세대 {generation} 최상 {best.fitness()} 평균\
                {mean(map(self._fitness_key, self._population))}')
            self._reproduce_and_replace()
            self._mutate()
            highest : C = max(self._population, key=self._fitness_key)
            if highest.fitness() > best.fitness():
                best = highest
        return best


class SimpleEquation(Chromosome):
    def __init__(self, x : int , y : int) -> None:
        self.x : int = x
        self.y : int = y
    
    def fitness(self) -> float:
        return 6 * self.x - self.x ** 2 + 4 * self.y - self.y ** 2
    
    @classmethod
    def random_instance(cls) -> SimpleEquation:
        return SimpleEquation(randrange(100), randrange(100))
    
    def crossover(self,
        other : SimpleEquation
        ) -> Tuple[SimpleEquation, SimpleEquation]:
        ## change y each other...
        child1 : SimpleEquation = deepcopy(self)
        child2 : SimpleEquation = deepcopy(other)
        
        child1.y = other.y
        child2.y = self.y

        return child1, child2
    
    def mutate(self) -> None:
        ## change x, y values...
        if random() > 0.5:
            if random () > 0.5:
                self.x += 1
            else:
                self.x -= 1
        else:
            if random() > 0.5:
                self.y += 1
            else:
                self.y -= 1