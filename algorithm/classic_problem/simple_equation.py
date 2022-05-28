from __future__ import annotations
from typing import List, Tuple
import sys
sys.path.insert(0, '.')
from genetic_algorithm import Chromosome, GeneticAlgorithm
from copy import deepcopy
from random import random, randrange

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
    
    def __str__(self) -> str:
        return f'X: {self.x} Y: {self.y} fitness: {self.fitness()}'


if __name__ == '__main__':
    ## start with 20 instances
    initial_population : List[SimpleEquation] = [SimpleEquation.random_instance()
        for _ in range(20)]
    
    genetic_algorithm : GeneticAlgorithm[SimpleEquation] = GeneticAlgorithm(
        initial_population=initial_population,
        threshold=13.0, max_generations=100,
        mutation_chance=0.1, crossover_chance=0.7)

    result : SimpleEquation = genetic_algorithm.run()
    
    print(result)