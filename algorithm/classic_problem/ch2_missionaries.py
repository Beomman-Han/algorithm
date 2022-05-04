from __future__ import annotations


MAX_NUM: int = 3

class MCState:
    """Missionaries problem
    1) Missionaries and cannibals are at the east of river.
    2) They have a boat where maximum two people can aboard.
    3) They should move from the west to the east safely.
    4) If the number of missionaries is smaller than cannibals,
    cannibals could eat missionaries.
    
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
    
    def __str__(self) -> str:
        ret_str = f'{self.wm} missionaries and {self.wc} cannibals at west.\n'
        ret_str += f'{self.em} missionaries and {self.ec} cannibals at east.\n'
        ret_str += f'boat are at {("west" if self.boat else "east")}'
        return ret_str