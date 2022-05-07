"""Constraint-Satisfaction Problem (CSP)
CSP consists of domain, variable, and contraint.
Variables are lacated at domain range with satisfying constraints.
"""

from abc import ABC, abstractmethod
from typing import Dict, Generic, List, Optional, TypeVar

V = TypeVar('V')  ## variable
D = TypeVar('D')  ## domain

class Constraint(Generic[V, D], ABC):
    ## constraint variable
    def __init__(self, variables: List[V]) -> None:
        self.variables = variables
    
    @abstractmethod
    def satisfied(self, assignment: Dict[V, D]) -> bool:
        ...


class CSP(Generic[V, D]):
    def __init__(self,
        variables: List[V],
        domains: Dict[V, List[D]]
        ) -> None:
        
        self.variables : List[V] = variables
        self.domains : Dict[V, List[D]] = domains
        self.constraints : Dict[V, List[Constraint[V, D]]] = {}
        ## check variable <- domain assignment
        for variable in self.variables:
            self.constraints[variable] = []
            if variable not in self.domains:
                raise LookupError('Domain must be assigned to all variables.')
        
    def add_constraint(self,
        constraint: Constraint[V, D]
        ) -> None:
        """Add constraint to variables"""
        
        for variable in constraint.variables:
            if variable not in self.variables:
                raise LookupError('Not constraint variable.')
            else:
                self.constraints[variable].append(constraint)
    
    def consistent(self,
        variable : V,
        assignment : Dict[V, D]
        ) -> bool:
        """Check all constraints are satisfied at all variables"""
        
        for constraint in self.constraints[variable]:
            if not constraint.satisfied(assignment):
                return False
        return True
    
    def backtracking_search(self,
        assignment : Dict[V, D] = {}
        ) -> Optional[Dict[V, D]]:
        """recursive dfs"""
        
        ## base case : all variables are assigned at assignment
        if len(assignment) == len(self.variables):
            return assignment
        
        ## all unassigned variables
        unassigned : List[V] = [ v for v in self.variables if v not in assignment ]
        
        ## bring all possible domains 
        ## from the first variable in unassigned
        first : V = unassigned[0]
        for domain in self.domains[first]:
            local_assignment = assignment.copy()
            local_assignment[first] = domain
            
            if self.consistent(first, local_assignment):
                result : Optional[Dict[V, D]] = self.backtracking_search(
                    local_assignment)
                if result is not None:
                    return result
        return None