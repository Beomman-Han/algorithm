from typing import Dict
from csp import Constraint, CSP

class MapColoringConstraint(Constraint[str, str]):
    """Solve map color problem where adjacent regions
    should not be painted with the same color.
    Variables are regions(total 7 regions), str type.
    Domains are colors for regions, only 3 colors, str type.
    Constraints are that adjacent variables must not have the same assignment.
    This is for setting the rule of constraints for adjacent variables."""
    
    def __init__(self, place1 : str, place2 : str) -> None:
        """Init with 2 variables, place1 and place2, which is adjacent places."""
        super().__init__([place1, place2])
        self.place1 = place1
        self.place2 = place2
    
    def satisfied(self, assignment: Dict[str, str]) -> bool:
        """Check whether 2 variables have the same domain (color).
        If 2 places have the same domain, return False, otherwise return True.
        If each variable is not assigned, return True."""
        
        if self.place1 not in assignment or self.place2 not in assignment:
            return True
        return assignment[self.place1] != assignment[self.place2]
