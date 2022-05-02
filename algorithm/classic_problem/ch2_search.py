"""
This is for practicing contents of searching problem
in Classic Computer Science Problem in Python.
"""

## find path at maze
from __future__ import annotations  ## allow 'Optional[Node]' code
from enum import Enum
import random
from collections import deque
from typing import Callable, Deque, Generic, List, NamedTuple, Optional, Protocol, Set, TypeVar


class Cell(str, Enum):
    """Represent status of each cell in maze"""
    EMPTY   = " "
    BLOCKED = "X"
    START   = "S"
    GOAL    = "G"
    PATH    = "*"


class MazeLocation(NamedTuple):
    """Inherit NamedTuple?
    
    namedtuple example:
    
    from collections import namedtuple
    MazeLocation = namedtuple('MazeLocation', ['row', 'column'])
    """
    
    row : int
    column : int


class Maze:
    def __init__(self,
        rows : int = 10,
        columns : int = 10,
        sparseness : float = 0.2,
        start : MazeLocation = MazeLocation(0, 0),
        goal : MazeLocation = MazeLocation(9, 9)
        ) -> None:
    
        self._rows = rows
        self._columns = columns
        self.start = start
        self.goal = goal
        
        self._grid: List[List[Cell]] = [[Cell.EMPTY for _ in range(columns)]
        for _ in range(rows)]
        
        self._randomly_fill(rows, columns, sparseness)
        
        self._grid[start.row][start.column] = Cell.START
        self._grid[goal.row][goal.column] = Cell.GOAL
        
        return        
    
    def _randomly_fill(self,
        rows : int,
        columns : int,
        sparseness : float
        ) -> None:
        
        """Fill Cell.BLOCKED at self._grid with some of sparseness"""
        
        for r in range(rows):
            for c in range(columns):
                if random.uniform(0, 1) < sparseness:
                    self._grid[r][c] = Cell.BLOCKED
        
        return
    
    def __str__(self) -> str:
        """Return string format of Maze instance"""
        
        output = ''
        for row in self._grid:
            output += "".join([item.value for item in row]) + '\n'
        return output

    def goal_test(self, loc : MazeLocation) -> bool:
        return loc == self.goal
    
    def _blocked_test(self,
        row : int,
        column : int
        ) -> bool:
        
        return self._grid[row][column] == Cell.BLOCKED
    
    def _check_bound(self, row: int, column: int) -> bool:
        return row in range(self._rows) and column in range(self._columns)
    
    def successors(self,
        loc : MazeLocation
        ) -> List[MazeLocation]:

        """Find all possible MazeLocation by List"""
        
        possible_locs = []
        if self._check_bound(loc.row + 1, loc.column) and \
            not self._blocked_test(loc.row + 1, loc.column):
            possible_locs.append(MazeLocation(loc.row + 1, loc.column))
        
        if self._check_bound(loc.row - 1, loc.column) and \
            not self._blocked_test(loc.row - 1, loc.column):
            possible_locs.append(MazeLocation(loc.row - 1, loc.column))
        
        if self._check_bound(loc.row, loc.column + 1) and \
            not self._blocked_test(loc.row, loc.column + 1):
            possible_locs.append(MazeLocation(loc.row, loc.column + 1))
        
        if self._check_bound(loc.row, loc.column - 1) and \
            not self._blocked_test(loc.row, loc.column - 1):
            possible_locs.append(MazeLocation(loc.row, loc.column - 1))
        
        return possible_locs
    
    def mark(self, path : List[MazeLocation]) -> None:
        """mark '*' on path from input list"""
        
        for loc in path:
            self._grid[loc.row][loc.column] = Cell.PATH
        ## re-mark start, goal position
        self._grid[self.start.row][self.start.column] = Cell.START
        self._grid[self.goal.row][self.goal.column] = Cell.GOAL
    
    def clear(self, path : List[MazeLocation]) -> None:
        """clear '*' marking on path"""
        
        for loc in path:
            self._grid[loc.row][loc.column] = Cell.EMPTY
        self._grid[self.start.row][self.start.column] = Cell.START
        self._grid[self.goal.row][self.goal.column] = Cell.GOAL


T = TypeVar('T')

class Node(Generic[T]):
    def __init__(self,
        state: T,
        #parent: Optional['Node'],
        parent: Optional[Node],
        cost: float = 0.0,
        heuristic: float =0.0
        ) -> None:
        
        self.state = state
        self.parent = parent
        self.cost = cost
        self.heuristic = heuristic  ## ??
    
    def __lt__(self, other: 'Node') -> bool:
        return (self.cost + self.heuristic) < (other.cost + other.heuristic)


class Stack(Generic[T]):
    """Stack abstract data structure implemented by python list"""
    
    def __init__(self) -> None:
        self._container: List[T] = []
    
    @property
    def empty(self) -> bool:
        return not self._container

    def push(self, item: T) -> None:
        self._container.append(item)
        
    def pop(self) -> T:
        return self._container.pop()
    
    def __str__(self) -> str:
        return repr(self._container)
    

def dfs(
    initial : T,
    goal_test : Callable[[T], bool],
    successors : Callable[[T], List[T]]
    ) -> Optional[Node[T]]:
    """Depth first search path from initial to goal"""
    
    frontier: Stack = Stack()
    explored: Set[T] = set()
    
    ## start to search path
    frontier.push(Node(initial, None))
    explored.add(initial)
    
    while not frontier.empty:
        current_node = frontier.pop()
        current_state = current_node.state
        if goal_test(current_state):
            return current_node
        for child in successors(current_state):
            if child not in explored:
                child_node = Node(child, current_node)
                frontier.push(child_node)
                explored.add(child)
    return None  ## could not find goal

def node_to_path(node: Node[T]) -> List[T]:
    """transform node connection info to list"""
    
    path: List[T] = []
    curr = node
    while curr:
        path.append(curr.state)
        curr = curr.parent
    path.reverse()
    return path


class Queue(Generic[T]):
    def __init__(self) -> None:
        self._container: Deque[T] = deque()
    
    @property
    def empty(self) -> bool:
        return not self._container
    
    def push(self, item: T) -> None:
        self._container.append(item)
    
    def pop(self) -> T:
        return self._container.popleft()
    
    def __repr__(self) -> str:
        return repr(self._container)


def bfs(
    initial : T,
    goal_test : Callable[[T], bool],
    successors : Callable[[T], List[T]]
    ) -> Optional[Node[T]]:
    """Breadth first search path from initial to goal"""
    
    frontier: Queue[Node[T]] = Queue()
    explored: Set[T] = set()
    
    ## start bfs
    frontier.push(Node(initial, None))
    explored.add(initial)
    
    while not frontier.empty:
        current_node = frontier.pop()
        current_state = current_node.state
        if goal_test(current_state):
            return current_node
        for neighbor in successors(current_state):
            if neighbor not in explored:
                frontier.push(Node(neighbor, current_node))
                explored.add(neighbor)
    return None