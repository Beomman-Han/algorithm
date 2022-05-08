from csp import Constraint, CSP

class MapColoringConstraint(Constraint[str, str]):
    """Solve map color problem where adjacent regions
    should not be painted with the same color."""