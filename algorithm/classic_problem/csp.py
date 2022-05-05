"""Constraint-Satisfaction Problem (CSP)
CSP consists of domain, variable, and contraint.
Variables are lacated at domain range with satisfying constraints.
"""

from abc import ABC, abstractmethod
from typing import Generic, List, TypeVar

V = TypeVar('V')  ## variable
D = TypeVar('D')  ## domain

class Constraint(Generic[V, D], ABC):
    ## constraint variable
    def __init__(self, variables: List[V]) -> None:
        self.variables = variables
    
    @abstractmethod
    def satisfied(self, assignment: Dict[V, D]) -> bool:
        ...