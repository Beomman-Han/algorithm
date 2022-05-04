from __future__ import annotations


MAX_NUM: int = 3

class MCState:
    """Missionaries and cannibals are at the east of river.
    The object is to move all missionaries from the east to the west safely.
    If the number of missionaries is smaller than cannibals,
    cannibals would eat missionaries...
    This is for solving missionaries and cannibals problem with path search algorithm.
    """
    
    def __init__(self,
        missionaries: int,
        cannibals: int,
        boat: bool
        ) -> None:
        
        self.wm = missionaries  ## missionaries at west
        self.wc = cannibals  ## cannibals at west
        self.em = MAX_NUM - missionaries  ## missionaries at east
        self.ec = MAX_NUM - cannibals  ## cannibals at east
        self.boat = boat