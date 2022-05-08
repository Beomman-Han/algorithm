from typing import Dict, List, Optional
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

if __name__ == "__main__":
    ## solve color mapping problem of AUS...
    ## with CSP and MapColoringConstraint object
    
    variables : List[str] = ['웨스턴 오스트레일리아', '노던 준주', '사우스 오스트레일리아', 
                           '퀸즐랜드', '뉴 사우스웨일스', '빅토리아', '태즈메이니아']
    domains : Dict[str, List[str]] = {region : ['빨강', '초록', '파랑'] for region in variables}
    
    csp : CSP[str, str] = CSP(variables, domains)

    csp.add_constraint(MapColoringConstraint('웨스턴 오스트레일리아', '노던 준주'))
    csp.add_constraint(MapColoringConstraint('웨스턴 오스트레일리아', '사우스 오스트레일리아'))
    
    csp.add_constraint(MapColoringConstraint('노던 준주', '사우스 오스트레일리아'))
    csp.add_constraint(MapColoringConstraint('노던 준주', '퀸즐랜드'))
    
    csp.add_constraint(MapColoringConstraint('사우스 오스트레일리아', '퀸즐랜드'))
    csp.add_constraint(MapColoringConstraint('사우스 오스트레일리아', '뉴 사우스웨일스'))
    csp.add_constraint(MapColoringConstraint('사우스 오스트레일리아', '빅토리아'))
    
    csp.add_constraint(MapColoringConstraint('퀸즐랜드', '뉴 사우스웨일스'))
    
    csp.add_constraint(MapColoringConstraint('뉴 사우스웨일스', '빅토리아'))
    
    csp.add_constraint(MapColoringConstraint('빅토리아', '태즈메이니아'))
    
    solution : Optional[Dict[str, str]] = csp.backtracking_search()
    print(solution)