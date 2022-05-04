from __future__ import annotations
from typing import List


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
        
        """Initialize MCState instance
        
        Parameters
        ----------
        missionaries : int
            # of missionaries at west
        cannibals : int
            # of cannibals at west
        boat : bool
            if True a boat is at west, else at east
        """
        
        self.wm = missionaries  ## missionaries at west
        self.wc = cannibals  ## cannibals at west
        self.em = MAX_NUM - missionaries  ## missionaries at east
        self.ec = MAX_NUM - cannibals  ## cannibals at east
        self.boat = boat  ## true : west, false : east
    
    def __str__(self) -> str:
        ret_str = f'{self.wm} missionaries and {self.wc} cannibals at west.\n'
        ret_str += f'{self.em} missionaries and {self.ec} cannibals at east.\n'
        ret_str += f'boat are at {("west" if self.boat else "east")}'
        return ret_str
    
    def goal_test(self) -> bool:
        return (self.em == MAX_NUM and self.ec == MAX_NUM)
    
    def _check_cannibalism(self) -> bool:
        return ((self.wm > 0 and self.wc > self.wm) or (self.em > 0 and self.ec > self.em))
        
    def successors(self) -> List[MCState]:
        possible_scenarios = []
        if self.wm + self.wc != 0:
            if self.boat:
                if self.wm - 1 >= 0:
                    state = MCState(self.wm - 1, self.wc, not self.boat)
                    possible_scenarios.append(state)  ## case 1
                    if self.wc - 1 >= 0:
                        state = MCState(self.wm - 1, self.wc - 1, not self.boat)
                        possible_scenarios.append(state)  ## case 2
                    if self.wm - 2 >= 0:
                        state = MCState(self.wm - 2, self.wc, not self.boat)
                        possible_scenarios.append(state)  ## case 3
                if self.wc - 1 >= 0:
                    state = MCState(self.wm, self.wc - 1, not self.boat)
                    possible_scenarios.append(state)  ## case 4
                    if self.wc - 2 >= 0:
                        state = MCState(self.wm, self.wc - 2, not self.boat)
                        possible_scenarios.append(state)  ## case 5
            else:
                if self.em - 1 >= 0:
                    state = MCState(self.wm + 1, self.wc, not self.boat)
                    possible_scenarios.append(state)
                    if self.ec - 1 >= 0:
                        state = MCState(self.wm + 1, self.wc + 1, not self.boat)
                        possible_scenarios.append(state)
                    if self.em - 2 >= 0:
                        state = MCState(self.wm + 2, self.wc, not self.boat)
                        possible_scenarios.append(state)
                if self.ec - 1 >= 0:
                    state = MCState(self.wm, self.wc + 1, not self.boat)
                    possible_scenarios.append(state)
                    if self.ec - 2 >= 0:
                        state = MCState(self.wm, self.wc + 2, not self.boat)
                        possible_scenarios.append(state)
        return [x for x in possible_scenarios if not x._check_cannibalism() ]